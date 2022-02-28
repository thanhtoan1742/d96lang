from D96Visitor import D96Visitor
from D96Parser import D96Parser
import AST

from functools import reduce
import operator


_initial_missing = object()
def sum_map(func, iterable, init = _initial_missing):
    "init is reduce's _initial_missing"
    return reduce(
        operator.add,
        map(func, iterable),
        init
    )


def parse_int(s: str) -> int:
    if s.startswith('0b') or s.startswith('0B'):
        return int(s[2:], 2)
    if s.startswith('0x') or s.startswith('0X'):
        return int(s[2:], 16)
    if s.startswith('0') and len(s) > 1:
        return int(s[1:], 8)
    return int(s)


class ASTGeneration(D96Visitor):
    def getKind(self, id: AST.Id):
        if id.name.startswith('$'):
            return AST.Static()
        return AST.Instance()


    def visitProgram(self, ctx: D96Parser.ProgramContext):
        return AST.Program([
            self.visit(c) for c in ctx.class_decl()
        ])


    def visitClass_decl(self, ctx: D96Parser.Class_declContext):
        className = AST.Id(ctx.ID(0).getText())
        parentName = AST.Id(ctx.ID(1).getText()) if ctx.COLON() else None
        memList = self.visit(ctx.class_mems())
        return AST.ClassDecl(className, memList, parentName)

    def visitClass_mems(self, ctx: D96Parser.Class_memsContext):
        attr_delcs = sum_map(
            lambda d: self.visit(d),
            ctx.attr_decl(),
            []
        )
        method_delcs = [self.visit(d) for d in ctx.method_decl()]
        return attr_delcs + method_delcs


    def visitAttr_decl(self, ctx: D96Parser.Attr_declContext):
        decls = self.visit(ctx.var_decl_mix())
        res = []
        for decl in decls:
            if isinstance(decl, AST.VarDecl):
                kind = self.getKind(decl.variable)
            else:
                kind = self.getKind(decl.constant)
            res.append(AST.AttributeDecl(kind, decl))
        return res



    def visitMethod_decl(self, ctx: D96Parser.Method_declContext):
        if ctx.normal_method_decl():
            return self.visit(ctx.normal_method_decl())
        if ctx.constuctor_decl():
            return self.visit(ctx.constuctor_decl())
        return self.visit(ctx.destuctor_decl())

    def visitNormal_method_decl(self, ctx: D96Parser.Normal_method_declContext):
        name = self.visit(ctx.mix_id())
        kind = self.getKind(name)
        param = self.visit(ctx.semi_param_decls())
        body = self.visit(ctx.stmt_block())
        return AST.MethodDecl(kind, name, param, body)

    def visitConstuctor_decl(self, ctx: D96Parser.Constuctor_declContext):
        name = AST.Id(ctx.CONSTRUCTOR().getText())
        kind = AST.Instance()
        param = self.visit(ctx.semi_param_decls())
        body = self.visit(ctx.stmt_block())
        return AST.MethodDecl(kind, name, param, body)

    def visitDestuctor_decl(self, ctx: D96Parser.Destuctor_declContext):
        name = AST.Id(ctx.DESTRUCTOR().getText())
        kind = AST.Instance()
        param = []
        body = self.visit(ctx.stmt_block())
        return AST.MethodDecl(kind, name, param, body)

    def visitSemi_param_decls(self, ctx: D96Parser.Semi_param_declsContext):
        decls = [self.visit(d) for d in ctx.param_decl()]
        if len(decls) == 0:
            return []
        return reduce(operator.add, decls)

    def visitParam_decl(self, ctx: D96Parser.Param_declContext):
        ids = self.visit(ctx.comma_ids())
        typ = self.visit(ctx.typ())
        return [AST.VarDecl(id, typ) for id in ids]


    def visitStmt_block(self, ctx: D96Parser.Stmt_blockContext):
        insts = sum_map(
            lambda s: self.visit(s),
            ctx.stmt(),
            []
        )
        return AST.Block(insts)

    def visitStmt(self, ctx: D96Parser.StmtContext):
        if ctx.var_decl_stmt():
            return self.visit(ctx.var_decl_stmt())
        stmt = ctx.assign_stmt() or \
            ctx.if_stmt() or \
            ctx.for_stmt() or \
            ctx.break_stmt() or \
            ctx.continue_stmt() or \
            ctx.return_stmt() or \
            ctx.method_ivk_stmt()
        return [self.visit(stmt)]


    def visitVar_decl_stmt(self, ctx: D96Parser.Var_decl_stmtContext):
        return self.visit(ctx.var_decl())


    def visitAssign_stmt(self, ctx: D96Parser.Assign_stmtContext):
        lhs = self.visit(ctx.lhs())
        exp = self.visit(ctx.exp())
        return AST.Assign(lhs, exp)

    def visitLhs(self, ctx: D96Parser.LhsContext):
        return self.visit(ctx.scalar_var() or ctx.idx_exp())

    # NOTE: is `Human::$count` a valid LHS
    def visitScalar_var(self, ctx: D96Parser.Scalar_varContext):
        id = AST.Id(ctx.ID().getText())
        if ctx.getChildCount() == 1:
            return id
        exp = self.visit(ctx.exp())
        return AST.FieldAccess(exp, id)

    def visitIdx_exp(self, ctx: D96Parser.Idx_expContext):
        arr = self.visit(ctx.exp8())
        idx = [self.visit(e) for e in ctx.exp()]
        return AST.ArrayCell(arr, idx)


    def visitIf_stmt(self, ctx: D96Parser.If_stmtContext):
        conds = [self.visit(c) for c in ctx.if_cond()]
        stmts = [self.visit(s) for s in ctx.stmt_block()]
        stmt = None if len(conds) == len(stmts) else stmts[-1]
        for i in reversed(range(len(conds))):
            stmt = AST.If(conds[i], stmts[i], stmt)
        return stmt

    def visitIf_cond(self, ctx: D96Parser.If_condContext):
        return self.visit(ctx.exp())


    def visitFor_stmt(self, ctx: D96Parser.For_stmtContext):
        id = self.visit(ctx.scalar_var())
        expr1 = self.visit(ctx.exp(0))
        expr2 = self.visit(ctx.exp(1))
        expr3 = self.visit(ctx.exp(2))
        body = self.visit(ctx.stmt_block())
        return AST.For(id, expr1, expr2, body, expr3)


    def visitBreak_stmt(self, ctx: D96Parser.Break_stmtContext):
        return AST.Break()


    def visitContinue_stmt(self, ctx: D96Parser.Continue_stmtContext):
        return AST.Continue()


    def visitReturn_stmt(self, ctx: D96Parser.Return_stmtContext):
        expr = self.visit(ctx.exp()) if ctx.exp() else None
        return AST.Return(expr)


    def visitMethod_ivk_stmt(self, ctx: D96Parser.Method_ivk_stmtContext):
        if ctx.DOT_OP():
            obj = self.visit(ctx.exp())
            method = AST.Id(ctx.ID().getText())
        else:
            obj = AST.Id(ctx.ID().getText())
            method = AST.Id(ctx.STATIC_ID().getText())
        param = self.visit(ctx.par_exps())
        return AST.CallStmt(obj, method, param)


    def visitVar_decl(self, ctx: D96Parser.Var_declContext):
        if self.visit(ctx.mut_mod()) == "Var":
            Decl = AST.VarDecl
        else:
            Decl = AST.ConstDecl
        ids, typ, values = self.visit(
            ctx.var_decl_init() or
            ctx.var_decl_no_init()
        )
        return [
            Decl(
                ids[i],
                typ,
                values[i] if i < len(values) else None,
            )
            for i in range(len(ids))
        ]

    def visitVar_decl_no_init(self, ctx: D96Parser.Var_decl_no_initContext):
        ids = self.visit(ctx.comma_ids())
        typ = self.visit(ctx.typ())
        return ids, typ, []

    def visitVar_decl_init(self, ctx: D96Parser.Var_decl_initContext):
        if ctx.EQ_OP():
            ids = self.visit(ctx.comma_ids())
            typ = self.visit(ctx.typ())
            values = [self.visit(ctx.exp())]
        else:
            id = AST.Id(ctx.ID().getText())
            value = self.visit(ctx.exp())
            ids, typ, values = self.visit(ctx.var_decl_init())
            ids = [id] + ids
            values = values + [value]

        return ids, typ, values


    def visitVar_decl_mix(self, ctx: D96Parser.Var_decl_mixContext):
        if self.visit(ctx.mut_mod()) == "Var":
            Decl = AST.VarDecl
        else:
            Decl = AST.ConstDecl
        ids, typ, values = self.visit(
            ctx.var_decl_init_mix() or
            ctx.var_decl_no_init_mix()
        )
        return [
            Decl(
                ids[i],
                typ,
                values[i] if i < len(values) else None,
            )
            for i in range(len(ids))
        ]

    def visitVar_decl_no_init_mix(self, ctx: D96Parser.Var_decl_no_init_mixContext):
        ids = self.visit(ctx.comma_mix_ids())
        typ = self.visit(ctx.typ())
        return ids, typ, []

    def visitVar_decl_init_mix(self, ctx: D96Parser.Var_decl_init_mixContext):
        if ctx.EQ_OP():
            ids = self.visit(ctx.comma_mix_ids())
            typ = self.visit(ctx.typ())
            values = [self.visit(ctx.exp())]
        else:
            id = self.visit(ctx.mix_id())
            value = self.visit(ctx.exp())
            ids, typ, values = self.visit(ctx.var_decl_init_mix())
            ids = [id] + ids
            values = values + [value]

        return ids, typ, values


    def visitMut_mod(self, ctx: D96Parser.Mut_modContext):
        if ctx.VAL():
            return "Val"
        else:
            return "Var"

    def visitComma_ids(self, ctx: D96Parser.Comma_idsContext):
        return [AST.Id(i.getText()) for i in ctx.ID()]

    def visitComma_mix_ids(self, ctx: D96Parser.Comma_mix_idsContext):
        return [self.visit(i) for i in ctx.mix_id()]

    def visitMix_id(self, ctx: D96Parser.Mix_idContext):
        token = ctx.ID() or ctx.STATIC_ID()
        return AST.Id(token.getText())


    def visitExp(self, ctx: D96Parser.ExpContext):
        return self.visit(ctx.exp0())

    def visitExp0(self, ctx: D96Parser.Exp0Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp1(0))
        op = (ctx.ADD_DOT_OP() or ctx.EQEQ_DOT_OP()).getText()
        left = self.visit(ctx.exp1(0))
        right = self.visit(ctx.exp1(1))
        return AST.BinaryOp(op, left, right)

    def visitExp1(self, ctx: D96Parser.Exp1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp2(0))
        op = (
            ctx.EQEQ_OP() or
            ctx.NOT_EQ_OP() or
            ctx.LT_OP() or
            ctx.GT_OP() or
            ctx.LE_OP() or
            ctx.GE_OP()
        ).getText()
        left = self.visit(ctx.exp2(0))
        right = self.visit(ctx.exp2(1))
        return AST.BinaryOp(op, left, right)

    def visitExp2(self, ctx: D96Parser.Exp2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp3())
        op = (ctx.AND_OP() or ctx.OR_OP()).getText()
        left = self.visit(ctx.exp2())
        right = self.visit(ctx.exp3())
        return AST.BinaryOp(op, left, right)

    def visitExp3(self, ctx: D96Parser.Exp3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp4())
        op = (ctx.ADD_OP() or ctx.SUB_OP()).getText()
        left = self.visit(ctx.exp3())
        right = self.visit(ctx.exp4())
        return AST.BinaryOp(op, left, right)

    def visitExp4(self, ctx: D96Parser.Exp4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp5())
        op = (ctx.MUL_OP() or ctx.DIV_OP() or ctx.MOD_OP()).getText()
        left = self.visit(ctx.exp4())
        right = self.visit(ctx.exp5())
        return AST.BinaryOp(op, left, right)

    def visitExp5(self, ctx: D96Parser.Exp5Context):
        exp = self.visit(ctx.exp6())
        if ctx.NOT_OP():
            return AST.UnaryOp(
                ctx.NOT_OP().getText(),
                exp
            )
        return exp

    def visitExp6(self, ctx: D96Parser.Exp6Context):
        exp = self.visit(ctx.exp7())
        if ctx.SUB_OP():
            return AST.UnaryOp(
                ctx.SUB_OP().getText(),
                exp
            )
        return exp

    def visitExp7(self, ctx: D96Parser.Exp7Context):
        exp = self.visit(ctx.exp8())
        if ctx.getChildCount() == 1:
            return exp
        idx = [self.visit(e) for e in ctx.exp()]
        return AST.ArrayCell(exp, idx)

    def visitExp8(self, ctx: D96Parser.Exp8Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp9())
        obj = self.visit(ctx.exp8())
        id = AST.Id(ctx.ID().getText())
        if ctx.par_exps():
            param = self.visit(ctx.par_exps())
            return AST.CallExpr(obj, id, param)
        return AST.FieldAccess(obj, id)

    # NOTE: There is no AST class for static access
    def visitExp9(self, ctx: D96Parser.Exp9Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp10())
        obj = AST.Id(ctx.ID().getText())
        id = AST.Id(ctx.STATIC_ID().getText())
        if ctx.par_exps():
            param = self.visit(ctx.par_exps())
            return AST.CallExpr(obj, id, param)
        return AST.FieldAccess(obj, id)

    def visitExp10(self, ctx: D96Parser.Exp10Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp11())
        className = AST.Id(ctx.ID().getText())
        param = self.visit(ctx.par_exps())
        return AST.NewExpr(className, param)

    def visitExp11(self, ctx: D96Parser.Exp11Context):
        if ctx.INT_LIT():
            return AST.IntLiteral(parse_int(ctx.INT_LIT().getText()))
        if ctx.FLOAT_LIT():
            return AST.FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        if ctx.STR_LIT():
            return AST.StringLiteral(ctx.STR_LIT().getText())
        if ctx.BOOL_LIT():
            return AST.BooleanLiteral(bool(ctx.BOOL_LIT().getText()))
        if ctx.NULL():
            return AST.NullLiteral()
        if ctx.SELF():
            return AST.SelfLiteral()
        return self.visit(ctx.arr() or ctx.mix_id() or ctx.exp())



    # NOTE: is ID a valid array cell init value
    def visitArr(self, ctx: D96Parser.ArrContext):
        values = self.visit(ctx.par_exps())
        return AST.ArrayLiteral(values)

    def visitPar_exps(self, ctx: D96Parser.Par_expsContext):
        return self.visit(ctx.comma_exps())

    def visitComma_exps(self, ctx: D96Parser.Comma_expsContext):
        return [self.visit(e) for e in ctx.exp()]


    def visitTyp(self, ctx: D96Parser.TypContext):
        return self.visit(
            ctx.prime_typ() or
            ctx.class_typ() or
            ctx.arr_typ()
        )

    def visitPrime_typ(self, ctx: D96Parser.Prime_typContext):
        if ctx.INT():
            return AST.IntType()
        if ctx.FLOAT():
            return AST.FloatType()
        if ctx.BOOL():
            return AST.BoolType()
        return AST.StringType()

    def visitClass_typ(self, ctx: D96Parser.Class_typContext):
        className = AST.Id(ctx.ID().getText())
        return AST.ClassType(className)

    # NOTE: VoidType???

    def visitArr_typ(self, ctx: D96Parser.Arr_typContext):
        size = int(ctx.INT_LIT().getText())
        eleType = self.visit(ctx.arr_typ() or ctx.prime_typ())
        return AST.ArrayType(size, eleType)
