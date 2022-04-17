import simulator1 as sim
import re
return_statements=[]
clock=0
stalls=0


class stages:
    def __init__(self,current_line,stalls_in_line,disassembled_instruction,forward):
        self.current_line=current_line
        self.stalls_in_line=stalls_in_line
        self.disassembled_instruction=[]
        self.forward=forward
        self.data=[]

    @staticmethod
    def instruction_breakdown(current_line):
        disassembled_instruction=[]
        print("Current Line: ",current_line)
        return_statements.append("Current Line: "+str(current_line))
        if(current_line<len(sim.lines)):
            line=sim.lines[current_line].strip()
            line=line.split(sep=" ")
            print("line ",line)
            return_statements.append("line "+str(line))
            if line[0]=='pass_PC':
                disassembled_instruction.append(line)
            else:
                line=line[0]+" "+line[1]
                disassembled_instruction.append(line)
            # for l in line[1]:
            #     l=l.strip()[1:]
            #     disassembled_instruction.append(l)

            return disassembled_instruction

    def check_stall(self,index_stage,current_line,existence_of_line=None):
        if existence_of_line is None:
            existence_of_line=[0,0,0]
        global stall

        s=0

        existence_of_line[0]=True
        existence_of_line[1]=(pipeline_stages[0].disassembled_instruction!=[])
        existence_of_line[2]=(pipeline_stages[1].disassembled_instruction!=[])

        if existence_of_line[2]:
            if pipeline_stages[2].disassembled_instruction=="pass_PC":
                pipeline_stages[0].current_line+=1
            else:    
                pipeline_stages[2].disassembled_instruction=pipeline_stages[1].disassembled_instruction.copy()
        
        if existence_of_line[1]:
            if pipeline_stages[1].disassembled_instruction=="pass_PC":
                pipeline_stages[0].current_line+=1
            else:
                pipeline_stages[1].disassembled_instruction=pipeline_stages[0].disassembled_instruction.copy()

        if existence_of_line[0]:
            if pipeline_stages[1].disassembled_instruction=="pass_PC":
                pipeline_stages[0].current_line+=1
            else:
                pipeline_stages[0].disassembled_instruction=self.instruction_breakdown(current_line)

        
        i=-1
        if existence_of_line[0]:
            i=0

        if existence_of_line[1]:
            i=1

        if existence_of_line[2]:
            i=2

        # Checking stalls for add and sub:
        if pipeline_stages[0].disassembled_instruction[0] in ("add","sub"):
            for j in range(1,i+1):

                if pipeline_stages[1].disassembled_instruction[0] in ("bne","beq"):
                    self.stalls_in_line+=1
                    stalls+=1
                    print("Stall: "+str(self.stalls_in_line),"in ", pipeline_stages[j].disassembled_instruction)
                    return_statements("Stall: "+str(self.stalls_in_line),"in ", str(pipeline_stages[j].disassembled_instruction))
                    s=1
                
                elif pipeline_stages[j].disassembled_instruction[0] in ("add","sub"):
                    print("Bazinga!")
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                    elif pipeline_stages[0].disassembled_instruction[3]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                
                elif pipeline_stages[j].disassembled_instruction[0] in ("sw"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[2]:
                        s=self.is_stall(j,False)
                
                elif pipeline_stages[j].disassembled_instruction[0] in ("lw"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,False)

                elif pipeline_stages[j].disassembled_instruction[0] in ("addi","sll"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                elif pipeline_stages[j].disassembled_instruction[0] in ("li"):
                    print("j ",j)
                    print(pipeline_stages[j].disassembled_instruction)
                    print(pipeline_stages[0].disassembled_instruction," Disassembly")
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                if s:
                    break

        # Checking stall for addi and sll:
        elif pipeline_stages[0].disassembled_instruction[0] in ("addi","sll"):
            for j in range(1,i+1):
                s=0

                if pipeline_stages[1].disassembled_instruction[0] in ("bne","beq"):
                    self.stalls_in_line+=1
                    stalls+=1
                    print("Stall: "+str(self.stalls_in_line),"in ", pipeline_stages[j].disassembled_instruction)
                    return_statements("Stall: "+str(self.stalls_in_line),"in ", str(pipeline_stages[j].disassembled_instruction))
                    s=1

                elif pipeline_stages[j].disassembled_instruction[0] in ("add","sub"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                elif pipeline_stages[j].disassembled_instruction[0] in ("sw"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[2]:
                        s=self.is_stall(j,False)

                elif pipeline_stages[j].disassembled_instruction[0] in ("lw"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,False)

                # Personal comment: Changed
                elif pipeline_stages[j].disassembled_instruction[0] in ("addi","sll","li"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                if s:
                    break
        # Checking stall for sw: 
        elif pipeline_stages[0].disassembled_instruction[0] =="sw":

            for j in range(1,i+1):
                s=0
                if pipeline_stages[1].disassembled_instruction[0] in ("bne","beq"):
                    self.stalls_in_line+=1
                    stalls+=1
                    print("Stall: "+str(self.stalls_in_line),"in ", pipeline_stages[j].disassembled_instruction)
                    return_statements("Stall: "+str(self.stalls_in_line),"in ", str(pipeline_stages[j].disassembled_instruction))
                    s=1

                elif pipeline_stages[j].disassembled_instruction[0] in ("add","sub"):
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                elif pipeline_stages[j].disassembled_instruction[0] in ("sw"):
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[2]:
                        s=self.is_stall(j,False)


                elif pipeline_stages[j].disassembled_instruction[0] in ("lw"):
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,False)

                elif pipeline_stages[j].disassembled_instruction[0] in ("addi","sll","li"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(k,self.forward)

                if s:
                    break

        elif pipeline_stages[0].disassembled_instruction[0] == "lw":

            for j in range(1,i+1):
                s=0
                if pipeline_stages[1].disassembled_instruction[0] in ("bne","beq"):
                    self.stalls_in_line+=1
                    stalls+=1
                    print("Stall: "+str(self.stalls_in_line),"in ", pipeline_stages[j].disassembled_instruction)
                    return_statements.append("Stall: "+str(self.stalls_in_line),"in ",str(pipeline_stages[j].disassembled_instruction))
                    s=1

                elif pipeline_stages[j].disassembled_instruction[0] in ("add","sub"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                elif pipeline_stages[j].disassembled_instruction[0] in ("sw"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[2]:
                        s=self.is_stall(j,False)


                elif pipeline_stages[j].disassembled_instruction[0] in ("lw"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,False)

                elif pipeline_stages[j].disassembled_instruction[0] in ("addi","sll","li"):
                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(k,self.forward)

                if s:
                    break

        # Checking stall in li:
        elif pipeline_stages[0].disassembled_instruction[0] == "li":
            for j in range(1,i+1):
                s=0
                if pipeline_stages[1].disassembled_instruction[0] in ("bne","beq"):
                    self.stalls_in_line+=1
                    stalls+=1
                    print("Stall: "+str(self.stalls_in_line),"in ", pipeline_stages[j].disassembled_instruction)
                    return_statements.append("Stall: "+str(self.stalls_in_line),"in ", str(pipeline_stages[j].disassembled_instruction))
                    s=1

                if s:
                    break

        # Checking stall in bne/beq:

        elif pipeline_stages[0].disassembled_instruction[0] in ("bne","beq"):
            for j in range(1,i+1):
                s=0
                if pipeline_stages[1].disassembled_instruction[0] in ("bne","beq"):
                    self.stalls_in_line+=1
                    stalls+=1
                    print("Stall: "+str(self.stalls_in_line),"in ", pipeline_stages[j].disassembled_instruction)
                    return_statements.append("Stall: "+str(self.stalls_in_line),"in ", str(pipeline_stages[j].disassembled_instruction))
                    s=1
                
                elif pipeline_stages[j].disassembled_instruction[0] in ("add","sub"):
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                    elif pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                elif pipeline_stages[j].disassembled_instruction[0] in ("sw"):
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[2]:
                        s-self.is_stall(j,False)

                    elif pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[2]:
                        s-self.is_stall(j,False)

                elif pipeline_stages[j].disassembled_instruction[0] in ("lw"):
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[1]:
                        s-self.is_stall(j,False)

                    elif pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s-self.is_stall(j,False)

                elif pipeline_stages[k].disassembled_instruction[0] in("addi","sll"):
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                    elif pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                elif pipeline_stages[k].disassembled_instruction[0] in ("li"):
                    if pipeline_stages[0].disassembled_instruction[1]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                    if pipeline_stages[0].disassembled_instruction[2]==pipeline_stages[j].disassembled_instruction[1]:
                        s=self.is_stall(j,self.forward)

                if s:
                    break

        return s

    @staticmethod
    def is_stall(dependent_instructions,forward):

        stall=0
        if dependent_instructions==1 and forward is False:
            stall+=2

        elif dependent_instructions==2 and forward is False:
            stall+=1

        elif dependent_instructions==1 and forward is True:
            stall+=1


        elif dependent_instructions==2 and forward is True:
            stall+=0

        print("Stalls: "+str(stall), "for ", pipeline_stages[0].disassembled_instruction)
        return_statements.append("Stalls: "+str(stall), "for ", pipeline_stages[0].disassembled_instruction)
        global stalls
        stalls+=stall
        return stall


#### Execution Starts #####

forward_enable=True
Program_done=False

sim.sanitize()
sim.process()
base_instruction_line=sim.line_counter

# if input("Do you want to enable data forwarding? (y/n): ").lower()=="y":
#     forward_enable=True
#     print("Data forwarding is enabled")
# else:
#     print("Data forwarding is disabled")

pipeline_stages=[
    # Following are our 5 stages of the pipeline
    stages(current_line=sim.line_counter,stalls_in_line=0,disassembled_instruction=[],forward=forward_enable),
    stages(current_line=sim.line_counter,stalls_in_line=0,disassembled_instruction=[],forward=forward_enable),
    stages(current_line=sim.line_counter,stalls_in_line=0,disassembled_instruction=[],forward=forward_enable),
    stages(current_line=sim.line_counter,stalls_in_line=0,disassembled_instruction=[],forward=forward_enable),
    stages(current_line=sim.line_counter,stalls_in_line=0,disassembled_instruction=[],forward=forward_enable)
]

def pass_nextStage(index_of_stage):
    pass
    # pipeline_stages[0].current_line+=1

def instruction_fetch():
    print("="*100)
    print(pipeline_stages[0].current_line)
    return_statements.append(pipeline_stages[0].current_line)
    print("="*100)
    print(len(sim.lines)," Length of lines")
    return_statements.append(str(len(sim.lines))+" Length of lines")

    if(pipeline_stages[0].current_line<len(sim.lines)):
        fetched_line=sim.lines[pipeline_stages[0].current_line]
        pipeline_stages[0].current_line+=1
        print(pipeline_stages[0].current_line," p[0].current_line")
        return_statements.append(str(pipeline_stages[0].current_line)+" p[0].current_line")
        return fetched_line

last_checked_stall_line=0

while not Program_done:
    for i in range(5):
        pipeline_stages[i].stalls_in_line=max(0,pipeline_stages[i].stalls_in_line-1)
        
        clock+=1
        print("="*100)
        print("Current Clock Cycle: ",clock)
        return_statements.append("Current Clock Cycle: "+str(clock))
        #==============================================================WB
        if len(pipeline_stages[4].data)<1:
            pass_nextStage(4)
            print("Passed WB")
            return_statements.append("Passed WB")
        
        else:
            (instruction_word,instruction_line,result)=pipeline_stages[4].data[0]
            pipeline_stages[4].data.pop(0)
            successful_write=1  

            if instruction_word not in ("sw","bne","beq"):
                if instruction_word in "lw":
                    result_mem=result
                    successful_write=sim.write_back_op(instruction_line,result_mem)

                elif instruction_word in ("add","sub","sll","li","addi"):
                    result_alu=result
                    successful_write=sim.write_back_op(instruction_line,result_alu)

                if successful_write==-1:
                    Program_done=True

            print("Executed WB on line ", instruction_line)
            return_statements.append("Executed WB on line "+str(instruction_line))
            ################################################################MEM

        if len(pipeline_stages[3].data)<1:
            pass_nextStage(3)
            print("Passed MEM")
            return_statements.append("Passed MEM")

        else:
            (instruction_word,instruction_line,result_alu)=pipeline_stages[3].data[0]
            pipeline_stages[3].data.pop(0)
            if instruction_word in ("lw","sw"):
                result_mem=sim.memory_op(instruction_word,instruction_line,result_alu)
                pipeline_stages[3].current_line-=1
                pipeline_stages[4].data.append((instruction_word,instruction_line,result_mem))
            else:
                pass_nextStage(3)
                pipeline_stages[4].data.append((instruction_word,instruction_line,result_alu))
            
            print("Executed Mem on line ", instruction_line)
            return_statements.append("Executed Mem on line "+str(instruction_line))
             ################################################################EX

        if len(pipeline_stages[2].data)<1:
            pass_nextStage(2)
            print("Pass Ex")
            return_statements.append("Pass Ex")
        else:
            (instruction_word,instruction_line)=pipeline_stages[2].data[0]
            pipeline_stages[2].data.pop(0)
            instruction_line=instruction_word+" "+instruction_line
            print("Instruction_line: ",instruction_line)
            print("Instruction_word: ",instruction_word)
            if instruction_word=='pass_PC' or instruction_line=='pass_PC':
                (result_alu,instruction_line)=(-1,instruction_line)
            else:
                (result_alu,instruction_line)=sim.execute_instructions(instruction_word,instruction_line)

            pipeline_stages[2].current_line-=1

            pipeline_stages[3].data.append((instruction_word,instruction_line,result_alu))
            if instruction_word in ("add","sub","li","addi","sll") and forward_enable:
                successful_write=sim.write_back_op(instruction_line,result_alu)

            print("Executed EX on line ",instruction_word,instruction_line)
            return_statements.append("Executed EX on line "+str(instruction_word)+str(instruction_line))
            ################################################################ID/RF

        if len(pipeline_stages[1].data)<1 or pipeline_stages[1].stalls_in_line:
            pass_nextStage(1)
            print("Passed ID/RF")
            return_statements.append("Passed ID/RF")
        else:

            no=["no",[0,0]]
            if(pipeline_stages[1].data[0]!=None):
                fetched_line=pipeline_stages[1].data[0]
                (instruction_word,instruction_line)=sim.find_typeof(fetched_line)
                if last_checked_stall_line!=pipeline_stages[0].current_line-1:
                    pipeline_stages[1].stalls_in_line+=pipeline_stages[1].check_stall(1,current_line=pipeline_stages[0].current_line-1)
                if pipeline_stages[1].stalls_in_line:
                    last_checked_stall_line=pipeline_stages[0].current_line-1
                    for i in range (pipeline_stages[1].stalls_in_line):
                        pipeline_stages[2].data.insert(0,no)

                    pipeline_stages[0].stalls_in_line=pipeline_stages[1].stalls_in_line
                    fetched_line=no

                else:
                    fetched_line=pipeline_stages[1].data[0]
                    pipeline_stages[1].data.pop(0)
                    (instruction_word,instruction_line)=sim.find_typeof(fetched_line)

                    pipeline_stages[2].data.append((instruction_word,instruction_line))

                    if instruction_word in ("bne","beq","j"):
                        if instruction_word=="bne":
                            return_bne_line=sim.bne(instruction_line,pipeline_stages[0].current_line-1)
                        if return_bne_line!=pipeline_stages[0].current_line:
                            pipeline_stages[0].current_line=return_bne_line
                            stalls+=1
                            pipeline_stages[0].stalls_in_line+=1

                        elif instruction_word=="beq":
                            return_bne_line=sim.beq(instruction_line,pipeline_stages[0].current_line-1)
                            if return_beq_line!=pipeline_stages[0].current_line:
                                pipeline_stages[0].current_line=return_beq_line
                                stalls+=1
                                pipeline_stages[0].stalls_in_line+=1

                            elif instruction_word=="j":
                                return_j_line=sim.j(instruction_line,pipeline_stages[0].current_line-1)
                            if return_j_line!=pipeline_stages[0].current_line:
                                pipeline_stages[0].current_line=return_j_line
                                stalls+=1
                                pipeline_stages[0].stalls_in_line+=1

            pipeline_stages[1].current_line-=1
            print("Executed ID/RF on line ",fetched_line)
            return_statements.append("Executed ID/RF on line "+str(fetched_line))
        #######################################################IF
        if pipeline_stages[0].stalls_in_line :
                clock+=0
        else:
            fetched_line=instruction_fetch()
            if(fetched_line=="end_PC"):
                Program_done=True
                break
            pipeline_stages[1].data.append(fetched_line)
            print("Executed IF on line: ",fetched_line)
            # if pipeline_stages[0].current_line==len(sim.lines):
            #     Program_done=True
            if len(pipeline_stages[1].data)==0 and len(pipeline_stages[2].data)==0 and len(pipeline_stages[3].data)==0 and len(pipeline_stages[4].data)==0 and pipeline_stages[0].current_line>=len(sim.lines):
                Program_done=True
            # if pipeline_stages[0].current_line==len(sim.lines):
            #     Program_done=True

        

       

        

        
        

        
sim.recursion()
# print("Final state of the memory: \n", sim.RAM)
# print("="*100)
# print("Register values after execution: \n",sim.registers)
# print("="*100)
print(pipeline_stages[0].stalls_in_line, " stalls_in_line")
return_statements.append(str(pipeline_stages[0].stalls_in_line)+ " stalls_in_line")
print("Total clock cycles taken: ",clock)
return_statements.append("Total clock cycles taken: "+str(clock))
print("Total Stalls: ",stalls)
return_statements.append("Total Stalls")



        

        