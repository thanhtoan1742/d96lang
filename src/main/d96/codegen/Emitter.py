from functools import reduce

import CodeGenerator as CG
import CodeGenError as CE
from MachineCode import JasminCode
from Frame import Frame
import AST


class EmitterException(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg
    def __str__(self) -> str:
        return "EmitterError:" + self.msg


def isAType(t: CG.Type) -> bool:
    return t in [CG.ArrayType, CG.ClassType, CG.StringType]


class Emitter:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.buff = list()
        self.jvm = JasminCode()

    def getJVMType(self, inType) -> str:
        typeIn = type(inType)
        if typeIn is CG.IntType:
            return "I"
        elif typeIn is CG.StringType:
            return "Ljava/lang/String;"
        elif typeIn is CG.VoidType:
            return "V"
        elif typeIn is CG.ArrayType:
            return "[" + self.getJVMType(inType.eleType)
        elif typeIn is CG.MethodType:
            return "(" + reduce(lambda acc, t: acc + self.getJVMType(t), inType.parTypes) + ")"\
                 + self.getJVMType(inType.retType)
        elif typeIn is CG.ClassType:
            return "L" + inType.className + ";"
        raise EmitterException("JVM type not recognized: " + str(typeIn))

    def emitPUSHICONST(self, inp, frame: Frame) -> str:
        #in: int or string
        #frame: Frame
        frame.push();
        if type(inp) is int:
            i = inp
            if i >= -1 and i <=5:
                return self.jvm.emitICONST(i)
            elif i >= -128 and i <= 127:
                return self.jvm.emitBIPUSH(i)
            elif i >= -32768 and i <= 32767:
                return self.jvm.emitSIPUSH(i)
        elif type(inp) is str:
            if inp == "true":
                return self.emitPUSHICONST(1, frame)
            elif inp == "false":
                return self.emitPUSHICONST(0, frame)
            else:
                return self.emitPUSHICONST(int(inp), frame)
        raise EmitterException("PUSHICONST type not recognized:" + str(type(inp)))

    def emitPUSHFCONST(self, inp: str, frame: Frame) -> str:
        #inp: String
        #frame: Frame
        f = float(inp)
        frame.push()
        rst = "{0:.4f}".format(f)
        if rst == "0.0" or rst == "1.0" or rst == "2.0":
            return self.jvm.emitFCONST(rst)
        else:
            return self.jvm.emitLDC(inp)

    '''
    *    generate code to push a constant onto the operand stack.
    *    @param in the lexeme of the constant
    *    @param typ the type of the constant
    '''
    def emitPUSHCONST(self, inp: str, typ, frame: Frame) -> str:
        #in_: String
        #typ: Type
        #frame: Frame
        if type(typ) is CG.IntType:
            return self.emitPUSHICONST(inp, frame)
        elif type(typ) is CG.StringType:
            frame.push()
            return self.jvm.emitLDC(inp)
        else:
            raise CE.IllegalOperandException(inp)

    def emitALOAD(self, inp: CG.Type, frame: Frame) -> str:
        #in_: Type
        #frame: Frame
        #..., arrayref, index, value -> ...
        frame.pop()
        if type(inp) is CG.IntType:
            return self.jvm.emitIALOAD()
        elif isAType(type(inp)):
            return self.jvm.emitAALOAD()
        else:
            raise CE.IllegalOperandException(str(inp))

    def emitASTORE(self, inp: CG.Type, frame: Frame) -> str:
        #in_: Type
        #frame: Frame
        #..., arrayref, index, value -> ...
        frame.pop()
        frame.pop()
        frame.pop()
        if type(inp) is CG.IntType:
            return self.jvm.emitIASTORE()
        elif isAType(type(inp)):
            return self.jvm.emitAASTORE()
        else:
            raise CE.IllegalOperandException(str(inp))

    '''    generate the var directive for a local variable.
    *   @param in the index of the local variable.
    *   @param varName the name of the local variable.
    *   @param inType the type of the local variable.
    *   @param fromLabel the starting label of the scope where the variable is active.
    *   @param toLabel the ending label  of the scope where the variable is active.
    '''
    def emitVAR(self, inp: int, varName: str, inType: CG.Type, fromLabel: int, toLabel: int, frame: Frame) -> str:
        #in_: Int
        #varName: String
        #inType: Type
        #fromLabel: Int
        #toLabel: Int
        #frame: Frame
        return self.jvm.emitVAR(inp, varName, self.getJVMType(inType), fromLabel, toLabel)

    def emitREADVAR(self, name: str, inType: CG.Type, index: int, frame: Frame) -> str:
        #name: String
        #inType: Type
        #index: Int
        #frame: Frame
        #... -> ..., value
        frame.push()
        if type(inType) is CG.IntType:
            return self.jvm.emitILOAD(index)
        elif isAType(type(inType)):
            return self.jvm.emitALOAD(index)
        else:
            raise CE.IllegalOperandException(name)

    ''' generate the second instruction for array cell access
    *
    '''
    def emitREADVAR2(self, name: str, typ: CG.Type, frame: Frame) -> str:
        #name: String
        #typ: Type
        #frame: Frame
        #... -> ..., value
        #frame.push()
        raise CE.IllegalOperandException(name)

    '''
    *   generate code to pop a value on top of the operand stack and store it to a block-scoped variable.
    *   @param name the symbol entry of the variable.
    '''
    def emitWRITEVAR(self, name: str, inType: CG.Type, index: int, frame: Frame) -> str:
        #name: String
        #inType: Type
        #index: Int
        #frame: Frame
        #..., value -> ...
        frame.pop()
        if type(inType) is CG.IntType:
            return self.jvm.emitISTORE(index)
        elif isAType(type(inType)):
            return self.jvm.emitASTORE(index)
        else:
            raise CE.IllegalOperandException(name)

    ''' generate the second instruction for array cell access
    *
    '''
    def emitWRITEVAR2(self, name: str, typ: CG.Type, frame: Frame) -> str:
        #name: String
        #typ: Type
        #frame: Frame
        #..., value -> ...
        #frame.push()
        raise CE.IllegalOperandException(name)

    ''' generate the field (static) directive for a class mutable or immutable attribute.
    *   @param lexeme the name of the attribute.
    *   @param in the type of the attribute.
    *   @param isFinal true in case of constant; false otherwise
    '''
    def emitATTRIBUTE(self, lexeme: str, inp: CG.Type, isFinal: bool, value: str) -> str:
        #lexeme: String
        #in_: Type
        #isFinal: Boolean
        #value: String
        return self.jvm.emitSTATICFIELD(lexeme, self.getJVMType(inp), False)

    def emitGETSTATIC(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        frame.push()
        return self.jvm.emitGETSTATIC(lexeme, self.getJVMType(inp))

    def emitPUTSTATIC(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        frame.pop()
        return self.jvm.emitPUTSTATIC(lexeme, self.getJVMType(inp))

    def emitGETFIELD(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        return self.jvm.emitGETFIELD(lexeme, self.getJVMType(inp))

    def emitPUTFIELD(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        frame.pop()
        frame.pop()
        return self.jvm.emitPUTFIELD(lexeme, self.getJVMType(inp))

    ''' generate code to invoke a static method
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name)
    *   @param in the type descriptor of the method.
    '''
    def emitINVOKESTATIC(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        typ = inp
        list(map(lambda x: frame.pop(), typ.parTypes))
        if not type(typ.retType) is CG.VoidType:
            frame.push()
        return self.jvm.emitINVOKESTATIC(lexeme, self.getJVMType(inp))

    ''' generate code to invoke a special method
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name)
    *   @param in the type descriptor of the method.
    '''
    def emitINVOKESPECIAL(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        if lexeme is not None and inp is not None:
            typ: CG.MethodType = inp
            list(map(lambda x: frame.pop(), typ.parTypes))
            frame.pop()
            if type(typ.retType) is not CG.VoidType:
               frame.push()
            return self.jvm.emitINVOKESPECIAL(lexeme, self.getJVMType(inp))
        elif lexeme is None and inp is None:
            frame.pop()
            return self.jvm.emitINVOKESPECIAL()
        raise EmitterException('INVOKE SPECIAL')

    ''' generate code to invoke a virtual method
    * @param lexeme the qualified name of the method(i.e., class-name/method-name)
    * @param in the type descriptor of the method.
    '''
    def emitINVOKEVIRTUAL(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        typ = inp
        list(map(lambda x: frame.pop(), typ.parTypes))
        frame.pop()
        if not type(typ) is CG.VoidType:
            frame.push()
        return self.jvm.emitINVOKEVIRTUAL(lexeme, self.getJVMType(inp))

    '''
    *   generate ineg, fneg.
    *   @param in the type of the operands.
    '''
    def emitNEGOP(self, inp: CG.Type, frame: Frame) -> str:
        #in_: Type
        #frame: Frame
        #..., value -> ..., result
        if type(inp) is CG.IntType:
            return self.jvm.emitINEG()
        else:
            return self.jvm.emitFNEG()

    def emitNOT(self, inp: CG.Type, frame: Frame) -> str:
        #in_: Type
        #frame: Frame
        label1 = frame.getNewLabel()
        label2 = frame.getNewLabel()
        result = list()
        result.append(self.emitIFTRUE(label1, frame))
        result.append(self.emitPUSHCONST("true", inp, frame))
        result.append(self.emitGOTO(label2, frame))
        result.append(self.emitLABEL(label1, frame))
        result.append(self.emitPUSHCONST("false", inp, frame))
        result.append(self.emitLABEL(label2, frame))
        return ''.join(result)

    '''
    *   generate iadd, isub, fadd or fsub.
    *   @param lexeme the lexeme of the operator.
    *   @param in the type of the operands.
    '''
    def emitADDOP(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        #..., value1, value2 -> ..., result
        frame.pop()
        if lexeme == "+":
            if type(inp) is CG.IntType:
                return self.jvm.emitIADD()
            else:
                return self.jvm.emitFADD()
        else:
            if type(inp) is CG.IntType:
                return self.jvm.emitISUB()
            else:
                return self.jvm.emitFSUB()

    '''
    *   generate imul, idiv, fmul or fdiv.
    *   @param lexeme the lexeme of the operator.
    *   @param in the type of the operands.
    '''
    def emitMULOP(self, lexeme: str, inp: CG.Type, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #frame: Frame
        #..., value1, value2 -> ..., result
        frame.pop()
        if lexeme == "*":
            if type(inp) is CG.IntType:
                return self.jvm.emitIMUL()
            else:
                return self.jvm.emitFMUL()
        else:
            if type(inp) is CG.IntType:
                return self.jvm.emitIDIV()
            else:
                return self.jvm.emitFDIV()

    def emitDIV(self, frame: Frame) -> str:
        #frame: Frame
        frame.pop()
        return self.jvm.emitIDIV()

    def emitMOD(self, frame: Frame) -> str:
        #frame: Frame
        frame.pop()
        return self.jvm.emitIREM()

    '''
    *   generate iand
    '''
    def emitANDOP(self, frame: Frame) -> str:
        #frame: Frame
        frame.pop()
        return self.jvm.emitIAND()

    '''
    *   generate ior
    '''
    def emitOROP(self, frame: Frame) -> str:
        #frame: Frame
        frame.pop()
        return self.jvm.emitIOR()

    def emitREOP(self, op: str, inp: CG.Type, frame: Frame) -> str:
        #op: String
        #in_: Type
        #frame: Frame
        #..., value1, value2 -> ..., result
        result = list()
        labelF = frame.getNewLabel()
        labelO = frame.getNewLabel()
        frame.pop()
        frame.pop()
        if op == ">":
            result.append(self.jvm.emitIFICMPLE(labelF))
        elif op == ">=":
            result.append(self.jvm.emitIFICMPLT(labelF))
        elif op == "<":
            result.append(self.jvm.emitIFICMPGE(labelF))
        elif op == "<=":
            result.append(self.jvm.emitIFICMPGT(labelF))
        elif op == "!=":
            result.append(self.jvm.emitIFICMPEQ(labelF))
        elif op == "==":
            result.append(self.jvm.emitIFICMPNE(labelF))
        result.append(self.emitPUSHCONST("1", CG.IntType(), frame))
        frame.pop()
        result.append(self.emitGOTO(labelO, frame))
        result.append(self.emitLABEL(labelF, frame))
        result.append(self.emitPUSHCONST("0", CG.IntType(), frame))
        result.append(self.emitLABEL(labelO, frame))
        return ''.join(result)

    def emitRELOP(self, op: str, inp: CG.Type, trueLabel: int, falseLabel: int, frame: Frame) -> str:
        #op: String
        #in_: Type
        #trueLabel: Int
        #falseLabel: Int
        #frame: Frame
        #..., value1, value2 -> ..., result
        result = list()
        frame.pop()
        frame.pop()
        if op == ">":
            result.append(self.jvm.emitIFICMPLE(falseLabel))
            result.append(self.emitGOTO(trueLabel, frame))
        elif op == ">=":
            result.append(self.jvm.emitIFICMPLT(falseLabel))
        elif op == "<":
            result.append(self.jvm.emitIFICMPGE(falseLabel))
        elif op == "<=":
            result.append(self.jvm.emitIFICMPGT(falseLabel))
        elif op == "!=":
            result.append(self.jvm.emitIFICMPEQ(falseLabel))
        elif op == "==":
            result.append(self.jvm.emitIFICMPNE(falseLabel))
        result.append(self.jvm.emitGOTO(trueLabel))
        return ''.join(result)

    '''   generate the method directive for a function.
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name).
    *   @param in the type descriptor of the method.
    *   @param isStatic <code>true</code> if the method is static; <code>false</code> otherwise.
    '''
    def emitMETHOD(self, lexeme: str, inp: CG.Type, isStatic:bool, frame: Frame) -> str:
        #lexeme: String
        #in_: Type
        #isStatic: Boolean
        #frame: Frame
        return self.jvm.emitMETHOD(lexeme, self.getJVMType(inp), isStatic)

    '''   generate the end directive for a function.
    '''
    def emitENDMETHOD(self, frame: Frame) -> str:
        #frame: Frame
        buffer = list()
        buffer.append(self.jvm.emitLIMITSTACK(frame.getMaxOpStackSize()))
        buffer.append(self.jvm.emitLIMITLOCAL(frame.getMaxIndex()))
        buffer.append(self.jvm.emitENDMETHOD())
        return ''.join(buffer)

    def getConst(self, ast: AST.AST):
        #ast: Literal
        if type(ast) is AST.IntLiteral:
            return (str(ast.value), CG.IntType())

    '''   generate code to initialize a local array variable.<p>
    *   @param index the index of the local variable.
    *   @param in the type of the local array variable.
    '''

    '''   generate code to initialize local array variables.
    *   @param in the list of symbol entries corresponding to local array variable.
    '''

    '''   generate code to jump to label if the value on top of operand stack is true.<p>
    *   ifgt label
    *   @param label the label where the execution continues if the value on top of stack is true.
    '''
    def emitIFTRUE(self, label: int, frame: Frame) -> str:
        #label: Int
        #frame: Frame
        frame.pop()
        return self.jvm.emitIFGT(label)

    '''
    *   generate code to jump to label if the value on top of operand stack is false.<p>
    *   ifle label
    *   @param label the label where the execution continues if the value on top of stack is false.
    '''
    def emitIFFALSE(self, label: int, frame: Frame) -> str:
        #label: Int
        #frame: Frame
        frame.pop()
        return self.jvm.emitIFLE(label)

    def emitIFICMPGT(self, label: int, frame: Frame) -> str:
        #label: Int
        #frame: Frame
        frame.pop()
        return self.jvm.emitIFICMPGT(label)

    def emitIFICMPLT(self, label: int, frame: Frame) -> str:
        #label: Int
        #frame: Frame
        frame.pop()
        return self.jvm.emitIFICMPLT(label)

    '''   generate code to duplicate the value on the top of the operand stack.<p>
    *   Stack:<p>
    *   Before: ...,value1<p>
    *   After:  ...,value1,value1<p>
    '''
    def emitDUP(self, frame: Frame) -> str:
        #frame: Frame
        frame.push()
        return self.jvm.emitDUP()

    def emitPOP(self, frame: Frame) -> str:
        #frame: Frame
        frame.pop()
        return self.jvm.emitPOP()

    '''   generate code to exchange an integer on top of stack to a floating-point number.
    '''
    def emitI2F(self, frame: Frame) -> str:
        #frame: Frame
        return self.jvm.emitI2F()

    ''' generate code to return.
    *   <ul>
    *   <li>ireturn if the type is IntegerType or BooleanType
    *   <li>freturn if the type is RealType
    *   <li>return if the type is null
    *   </ul>
    *   @param in the type of the returned expression.
    '''

    def emitRETURN(self, inp: CG.Type, frame: Frame) -> str:
        #in_: Type
        #frame: Frame
        if type(inp) is CG.IntType:
            frame.pop()
            return self.jvm.emitIRETURN()
        elif type(inp) is CG.VoidType:
            return self.jvm.emitRETURN()

    ''' generate code that represents a label
    *   @param label the label
    *   @return code Label<label>:
    '''
    def emitLABEL(self, label: int, frame: Frame) -> str:
        #label: Int
        #frame: Frame
        return self.jvm.emitLABEL(label)

    ''' generate code to jump to a label
    *   @param label the label
    *   @return code goto Label<label>
    '''
    def emitGOTO(self, label: int, frame: Frame) -> str:
        #label: Int
        #frame: Frame
        return self.jvm.emitGOTO(label)

    ''' generate some starting directives for a class.<p>
    *   .source MPC.CLASSNAME.java<p>
    *   .class public MPC.CLASSNAME<p>
    *   .super java/lang/Object<p>
    '''
    def emitPROLOG(self, name: str, parent: str) -> str:
        #name: String
        #parent: String
        result = list()
        result.append(self.jvm.emitSOURCE(name + ".java"))
        result.append(self.jvm.emitCLASS("public " + name))
        result.append(self.jvm.emitSUPER("java/land/Object" if parent == "" else parent))
        return ''.join(result)

    def emitLIMITSTACK(self, num: int) -> str:
        #num: Int
        return self.jvm.emitLIMITSTACK(num)

    def emitLIMITLOCAL(self, num: int) -> str:
        #num: Int
        return self.jvm.emitLIMITLOCAL(num)

    def emitEPILOG(self):
        file = open(self.filename, "w")
        file.write(''.join(self.buff))
        file.close()

    ''' print out the code to screen
    *   @param in the code to be printed out
    '''
    def printout(self, inp: str) -> None:
        #in_: String
        self.buff.append(inp)

    def clearBuff(self) -> None:
        self.buff.clear()
