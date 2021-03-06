import os
import subprocess
import json
from termcolor import colored as clr , cprint
import time
from itertools import zip_longest
from tqdm import tqdm

cp_keys = ['-cp','-Cp']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class Cp_my_tester:

    TLE = 4

    def diff_print(self,name,value):
        print('  '+name+' :')
        for x in value:
            x = '  '+ x
            print(x)
        
    def different(self,value,output,expected,case):
        x = output.split('\n')
        y = expected.split('\n')
        i = value.split('\n')
        pt  = '  '+'-'*5+'Problem Found in '+case+'-'*5
        cprint(pt,'yellow')
        # print('Input :')
        # print(value)
        self.diff_print('Input',i)
        self.diff_print('Output',x)
        self.diff_print('Expected',y)
        # print('Output :')
        # print(output)
        # print("Expected :")
        # print(expected)
        print("  Difference :")
        for wx,wy in zip_longest(x,y,fillvalue=''):
            print('  ',end='')
            for o , e in zip_longest(wx,wy,fillvalue=''):
                if(o == e):
                    cprint(o,'green',end='')
                else :
                    cprint(o,'red',end='')
                    cprint(e,'yellow',end='')
            print()
        cprint('  '+'-'*(len(pt)-2),'yellow')

    # def sub_process(self,cmd,value):
    #     tle = False
    #     try :
    #         x = subprocess.call(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,timeout=self.TLE)
    #         with x.stdin as f:
    #             f.write(value.encode())
    #             result = (x.communicate()[0]).decode('utf-8')
    #     except :
    #         result = "$TLE$"
    #         tle = True
    #     return (result,tle)


    def sub_process(self,cmd,value):

        x = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        with x.stdin as f:
            f.write(value.encode())
            result = (x.communicate()[0]).decode('utf-8')
            # print(result)
        
        return (result,False)

    def test(self,file_name):
        path = os.getcwd()
        # print(path, file_name)
        pt='-'*20+file_name+'-'*20
        cprint(pt,'magenta')
        pt = (' '*17+"...Testing...")
        cprint(pt,'blue')
        print()

        if not os.path.isdir('test'):
            cprint("Test folder not available.",'red',attrs=['bold'])
            return
        
        file_path = os.path.join(path,'test')
        lt = os.listdir(file_path)
        # print(lt)
        if len(lt) == 0 :
            cprint('Not test file available.')
            return 
        ext = file_name.rsplit(sep='.',maxsplit=1)
        type = ''
        if len(ext) > 1 :
            if ext[1] == 'cpp':
                type = 'cpp'
            elif ext[1] == 'py':
                type = 'py'
        
        if type == 'cpp':
            cmd = f"g++ '{file_name}' -o test.out"
            t = time.time()
            os.system(cmd)
            t = time.time() - t
            t = '{:.4f}'.format(t)
            pt = (f' #  Compilation time {t} s')
            cprint(pt,'blue')
        passed = 0 
        failed = 0
        test_files =[]
        cases = 0
        for file in lt:
            ext = file.rsplit(sep='.',maxsplit=1)
            # print(f'file = {ext}')
            try :
                if ext[1] == 'in':
                    out = ext[0] + '.out'
                    if os.path.isfile(os.path.join(file_path,out)):
                        test_files.append((file,out))
                        cases += 1
                    else:
                        # print(f'{out} not found.')
                        pass
            except :
                pass
        if cases == 0:
            cprint(" # No testcase available.",'red')
            return
        if cases == 1:
            cprint(" # 1 testcase found.",'yellow')
        else :
            cprint(f' # {cases} testcases found','yellow')

        st = -1.0
        slowest = ''
        is_tle = False
        for f in test_files:
            file = f[0]
            out = f[1]
            # print(f'testing {file} with {out}')
            ext = file.rsplit(sep='.',maxsplit=1)
            with open(os.path.join(file_path,file),'r') as f:
                value = f.read()
            t = time.time()
            if type == 'cpp':
                result = self.sub_process(['./test.out'],value)
            elif type =='py':
                result = self.sub_process(['python3',file_name],value)
            else:
                result = ('',False)
            tle = result[1]
            result = result[0]

            t = time.time() - t
            if t > st:
                st = t
                slowest = ext[0]
            # t = '{:.4}'.format(t)
            t = f'{t:.4f}'
            # print('code :\n',result)
            print()
            cprint('  * '+ext[0],'yellow')
            cprint('  * Time : ','cyan',end='')
            if tle :
                cprint('TLE','red')
                is_tle = True
            else :
                cprint(t,'cyan')
            
            with open(os.path.join(file_path,out)) as f:
                ans = f.read()
            # print('Expected :\n',ans)
            if result == ans:
                cprint('  * Passed','green')
                passed += 1
            else :
                cprint('  * WA','red')
                failed += 1
                if tle == False:
                    self.different(value,result,ans,ext[0])
                else :
                    is_tle = True

        print()
        st = f'{st:.4f}'
        pt = f' # Slowest : '
        cprint(pt,'blue', end='')
        if is_tle :
            cprint('TLE','red',end='')
        else :
            cprint(st,'blue',end='')
        cprint(' ['+slowest+']','blue')
        
        pt = (f' # Status : {passed}/{passed+failed} (AC/Total)')
        cprint(pt,'yellow')
        if failed == 0:
            cprint(" # Passed....",'green')
        else :
            cprint(" # Failed....",'red')

        os.remove('test.out')
        print()
        pt='-'*20+'-'*len(file_name)+'-'*20
        cprint(pt,'magenta')

    def find_files(self,file_name=''):

        file_list = []
        # print(file_name)
        supported_ext = ['cpp','py']
        # print(os.getcwd)
        for file in os.listdir(os.getcwd()):
            try :
                ext = file.rsplit(sep='.',maxsplit=1)
                for i in supported_ext:
                    if ext[1] == i:
                        if file_name in file:
                            file_list.append(file)
            except:
                pass
        # print(file_list)
        sz = len(file_list)
        if sz == 1:
            self.test(file_list[0])
        elif sz > 1:
            no = 1
            cprint("All the available files are given below.\n",'yellow')
            for file in file_list:
                pt = (' '*4+str(no)+') '+file)
                cprint(pt,'blue')
                no += 1
            cprint(' '*4+'0) Cancel operation','red')
            print()
            while True:
                cprint("Select the file index : ",'cyan',end='')
                index = int(input())
                if index == 0:
                    cprint("Testing operation cancelled.",'red')
                    break
                elif index < no:
                    self.test(file_list[index-1])
                    break
                else:
                    cprint("You have entered the wrong index.Please try again.",'red')
        else :
            cprint("NO FILE FOUND :(",'red')



class Cp_Problem:

    def fetch_problem(self,url = ''):
        try :
            cprint(' '*17+'...Parsing Problem...'+' '*17,'blue')
            if url == '':
                cprint('Enter the url : ','cyan',end='')
                url = input()
            cprint('-'*55,'magenta')
            # os.system(cmd)
            cmd = 'oj-api get-problem ' + url
            cmd = list(cmd.split())

            cp = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            problem = json.loads(cp.stdout)
            # with open('problem.json','w') as f:
            #     f.write(cp.stdout)

            

            if problem['status'] == 'ok':
                # print('ok')
                try :
                    alphabet = problem['result']['context']['alphabet']
                except :
                    alphabet = ''
                problem_name = problem['result']['name']
                problem_name = alphabet + '-'+problem_name
                # print(problem_name)
                if not os.path.isdir(problem_name):
                    os.mkdir(problem_name)
                try:
                    result = f"\tFetched '{problem_name}' Successfully"
                    testcases = problem['result']['tests']
                    # print(testcases)
                    # if not os.path.isdir(problem_name):
                    # os.mkdir("'"+problem_name+"'"+'/test')
                    base = os.getcwd()
                    path = os.path.join(base,problem_name,"")

                    info = '{"name" : "$NAME" , "url" : "$URL" }'

                    info = info.replace('$NAME',problem_name)
                    info = info.replace('$URL',url)

                    with open(path+'.info','w') as f:
                        f.write(info)
                    
                    # print(path)
                    if not os.path.isdir(path+"test"):
                        os.mkdir(path+"test")
                    path = os.path.join(path,'test')
                    no = 1
                    for case in testcases:
                        # print(case)
                        fileName_in = 'Sample-'+str(no).zfill(2)+'.in'
                        fileName_out = 'Sample-'+str(no).zfill(2)+'.out'
                        # print(fileName_in)
                        no += 1
                        with open(os.path.join(path,fileName_in),'w') as fin:
                            fin.write(case['input'])
                        with open(os.path.join(path,fileName_out) ,'w') as fout:
                            fout.write(case['output'])
                    cprint(result,'green')

                except Exception as e:
                    print(e)
                
            else :
                result = "Wrong url."
                cprint(result,'result')

            cprint('-'*55,'magenta')
            
        except Exception as e:
            print('-'*55)
            # print(e)
            cprint("Sorry Can't Fetch.",'red')


class Cp_login:

    def login(self):
        try :
            cprint(' '*17+'...Log In Service...'+' '*17,'blue')
            cprint('Enter judge link : ','cyan',end='')
            oj = input()
            cprint('Enter your username : ','cyan',end='')
            username = input()
            cprint('Enter your password : ','cyan',end='')
            password = input()
            cmd = "USERNAME=$USERNAME PASSWORD=$PASS oj-api login-service " + oj + '> .status'
            cmd = cmd.replace("$USERNAME",username) 
            cmd = cmd.replace("$PASS",password) 
            # print(cmd)
            os.system(cmd)
            with open('.status','r') as f:
                cp = f.read()
            cp = json.loads(cp)
            if cp["result"]['loggedIn']:
                cprint("Logged in successfully....",'green')
            else :
                cprint("Login failed.",'red')
            os.remove('.status')
        except Exception as e:
            # print(e)
            cprint("Login failed. (Sad)",'red')
            pass

class Cp_Test:

    def test_it(self, file_name):
        try :
            pt='-'*20+file_name+'-'*20
            cprint(pt,'magenta')
            pt = (' '*17+"...Testing...")
            print(clr(pt,'blue'))
            cmd = "g++ "+file_name+" && oj t"
            # cmd = 'g++ '+file_name+' -o a.out'
            os.system(cmd)
            # cmd_all =[['g++',file_name,'-o','a.out'] , ['oj','t']]
            # cmd_all =[['oj','t']]
            # print(cmd)
            # for i in cmd_all:
            #     cp = subprocess.run(i, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # result = cp.stderr
            # result = result.replace('test failed',clr('test failed','red'))
            # result = result.replace('WA',clr('WA','red'))
            # result = result.replace('AC',clr('AC','green'))
            # print(result)
            pt = ('-'*20+'-'*len(file_name)+'-'*20)
            cprint(pt,'magenta')
        except Exception as e:
            print(e)
            cprint("Got some error. :(",'red')

    def find_files(self,file_name=''):

        file_list = []
        # print(file_name)
        supported_ext = ['cpp','py']
        # print(os.getcwd)
        for file in os.listdir(os.getcwd()):
            try :
                ext = file.rsplit(sep='.',maxsplit=1)
                for i in supported_ext:
                    if ext[1] == i:
                        if file_name in file:
                            file_list.append(file)
            except:
                pass
        # print(file_list)
        sz = len(file_list)
        if sz == 1:
            self.test_it(file_list[0])
        elif sz > 1:
            no = 1
            cprint("All the available files are given below.\n",'yellow')
            for file in file_list:
                pt = (' '*4+str(no)+') '+file)
                cprint(pt,'blue')
                no += 1
            cprint(' '*4+'0) Cancel operation','red')
            print()
            while True:
                cprint("Select the file index : ",'cyan',end='')
                index = int(input())
                if index == 0:
                    cprint("Testing operation cancelled.",'red')
                    break
                elif index < no:
                    self.test_it(file_list[index-1])
                    break
                else:
                    cprint("You have entered the wrong index.Please try again.",'red')
        else :
            cprint("NO FILE FOUND :(",'red')


class Cp_Submit:

    def submit_it(self,file_name):
        try :
            with open('.info','r') as f:
                info = f.read()
            info = json.loads(info)
            problem_name = info['name']
            url = info['url']
        except :
            cprint("Enter the problem url : ",'cyan',end='')
            url = input()
            problem_name = url
        pt = '-'*20+'Problem Description'+'-'*20
        cprint(pt,'magenta')
        cprint(' '*4+'Problem : ','yellow',end='')
        cprint(problem_name,'green')
        cprint(' '*4+'Problem url: ','yellow',end='')
        cprint(url,'green')
        cprint(' '*4+'File name: ','yellow',end='')
        cprint(file_name,'green')
        cprint('-'*len(pt),'magenta')
        cprint('Enter (y/n) to confirm : ','yellow',attrs=['bold'],end='')
        x = input()
        if x.lower() == 'y':
            cprint('Submitting...','green')
            cmd = 'oj submit --wait=0 --yes $URL $FILENAME'
            cmd = cmd.replace('$URL',url)
            cmd = cmd.replace('$FILENAME',file_name)
            os.system(cmd)
        else :
            cprint('Submitting Cancelled.','red')

    def find_files(self,file_name=''):
        cprint(' '*17+'...Submitting Problem...'+'\n','blue')
        file_list = []
        # print(f'FIle name is {file_name}')
        supported_ext = ['cpp','py']
        for file in os.listdir(os.getcwd()):
            try :
                ext = file.rsplit(sep='.',maxsplit=1)
                for i in supported_ext:
                    if ext[1] == i:
                        if file_name in file:
                            file_list.append(file)
            except:
                pass
        # print(file_list)
        sz = len(file_list)
        if sz == 1:
            self.submit_it(file_list[0])
        elif sz > 1:
            no = 1
            cprint("All the available files are given below.\n",'yellow')
            for file in file_list:
                pt = (' '*4+str(no)+') '+file)
                cprint(pt,'blue')
                no += 1
            cprint(' '*4+'0) Cancel operation','red')
            print()
            while True:
                cprint("Select the file number : ",'cyan',end='')
                index = int(input())
                if index == 0:
                    cprint("Submitting operation cancelled.",'red')
                    break
                elif index < no:
                    self.submit_it(file_list[index-1])
                    break
                else:
                    cprint("You have entered the wrong index.Please try again.",'red')
        else :
            cprint("NO FILE FOUND :(",'red')

class Cp_add_test:

    @property
    def take_input(self):
        content = ''
        while True:
            try :
                line = input()
            except EOFError:
                break
            content += line +'\n'

        return content


    def add_case(self , no = 1,name='Custom-'):
        """  function for adding testcases """
        try :
            pt='-'*20+'-'*10+'-'*20
            cprint(pt,'magenta')
            pt = (' '*17+"...Adding Testcase..."+'\n')
            print(clr(pt,'blue'))
            
            if not os.path.isdir('test'):
                os.mkdir('test')
            path_name = os.path.join(os.getcwd(),'test')
            # print(path_name)
            lt = os.listdir(path_name)
            # print(lt)
            ase = len(lt)
            no = int(ase/2)+1

            cprint('Enter the input(Press Ctrl+d or Ctrl+z after done):','yellow')
            x = self.take_input

            cprint('Enter the output(Press Ctrl+d or Ctrl+z after done):','yellow')
            y = self.take_input


            fileName_in = name+str(no).zfill(2)+'.in'
            fileName_out = name+str(no).zfill(2)+'.out'
            # print(fileName_in)
            no += 1
            with open(os.path.join(path_name,fileName_in),'w') as fin:
                fin.write(x)
            with open(os.path.join(path_name,fileName_out) ,'w') as fout:
                fout.write(y)

            cprint('Testcase added Sucessfully. :D','green',attrs=['bold'])

            pt='-'*20+'-'*10+'-'*20
            cprint(pt,'magenta')
        except:
            cprint("Can't add testcase. :( ",'red',attrs=['bold'])


class Cp_bruteforce:

    def find_files(self,file_name=''):
        
        file_list = []
        # print(f'FIle name is {file_name}')
        supported_ext = ['cpp','py']
        for file in os.listdir(os.getcwd()):
            try :
                ext = file.rsplit(sep='.',maxsplit=1)
                for i in supported_ext:
                    if ext[1] == i:
                        if file_name in file:
                            file_list.append(file)
            except:
                pass
        # print(file_list)
        sz = len(file_list)
        if sz == 1:
            return (file_list[0],True)
        elif sz > 1:
            xp = file_name
            if xp == '':
                xp = 'test'
            cprint(' '*17+'...Choose '+xp +' file...'+'\n','blue')
            no = 1
            cprint("All the available files are given below.\n",'yellow')
            for file in file_list:
                pt = (' '*4+str(no)+') '+file)
                cprint(pt,'blue')
                no += 1
            cprint(' '*4+'0) Cancel operation','red')
            print()
            while True:
                cprint("Select the file number : ",'cyan',end='')
                index = int(input())
                if index == 0:
                    cprint("Bruteforcing operation cancelled.",'red')
                    return ('Cancelled',False)
                    break
                elif index < no:
                    return (file_list[index-1],True)
                    break
                else:
                    cprint("You have entered the wrong index.Please try again.",'red')
        else :
            cprint("NO FILE FOUND :(",'red')
            return ('FILE NOT FOUND',False)

    def diff_print(self,name,value):
        print('  '+name+' :')
        for x in value:
            x = '  '+ x
            print(x)
        
    def different(self,value,output,expected):
        x = output.split('\n')
        y = expected.split('\n')
        i = value.split('\n')
        pt  = '  '+'-'*5+'Problem Found'+'-'*5
        cprint(pt,'yellow')
        # print('Input :')
        # print(value)
        self.diff_print('Input',i)
        self.diff_print('Output',x)
        self.diff_print('Expected',y)
        # print('Output :')
        # print(output)
        # print("Expected :")
        # print(expected)
        print("  Difference :")
        for wx,wy in zip_longest(x,y,fillvalue=''):
            print('  ',end='')
            for o , e in zip_longest(wx,wy,fillvalue=''):
                if(o == e):
                    cprint(o,'green',end='')
                else :
                    cprint(o,'red',end='')
                    cprint(e,'yellow',end='')
            print()
        cprint('  '+'-'*(len(pt)-2),'yellow')



    def sub_process(self,cmd,value,iput):

        x = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        # print('here')
        with x.stdin as f:
            if iput:
                f.write(value.encode())
            result = (x.communicate()[0]).decode('utf-8')
            # print(result)
        
        return (result,False)

    def cmd_manager(self,file_name,value,ext,iput = True):
        pass
        if ext == 'py':
            cmd = ['python3',file_name]
        elif ext == 'cpp':
            ext = file_name.rsplit(sep='.',maxsplit=1)
            cmd = './'+ext[0]
            cmd = [cmd]
        else:
            cprint('command manager failed.','red')
            return ''
        # print(cmd)
        return self.sub_process(cmd,value,iput)[0]


    def add_case(self ,x,y, no = 1,name='Genarated-'):
        """  function for adding testcases """
        try :
            
            if not os.path.isdir('test'):
                os.mkdir('test')
            path_name = os.path.join(os.getcwd(),'test')
            # print(path_name)
            lt = os.listdir(path_name)
            # print(lt)
            ase = len(lt)
            no = int(ase/2)+1

            fileName_in = name+str(no).zfill(2)+'.in'
            fileName_out = name+str(no).zfill(2)+'.out'
            # print(fileName_in)
            no += 1
            with open(os.path.join(path_name,fileName_in),'w') as fin:
                fin.write(x)
            with open(os.path.join(path_name,fileName_out) ,'w') as fout:
                fout.write(y)

            cprint('Testcase added Sucessfully. :D','green',attrs=['bold'])

        except:
            cprint("Can't add testcase. :( ",'red',attrs=['bold'])

    def run(self):
        pass
        
        brute_file = self.find_files('brute')
        # print(brute_file)
        if brute_file[1] == False:
            return
        # print(brute_file[0])
        gen_file = self.find_files('gen')
        # print(gen_file)
        # print(gen_file[1])
        if gen_file[1] == False:
            return
        test_file = self.find_files('')
        if test_file[1] == False:
            return

        test_file = test_file[0]
        brute_file = brute_file[0]
        gen_file = gen_file[0]
        # print(test_file)
        cprint('How many times do you want to stress? : ','cyan',end ='')
        no = int(input())
        if no < 1:
            cprint('You want to bruteforce test less than 1 time? Seriously man? (-_-)','red')
            return
        # testing....
        print()
        brute_ext = brute_file.rsplit(sep='.',maxsplit=1)[1]
        gen_ext = gen_file.rsplit(sep='.',maxsplit=1)[1]
        test_ext = test_file.rsplit(sep='.',maxsplit=1)[1]
        # print(brute_ext,gen_ext,test_ext)
        if brute_ext == 'cpp':
            # print('cpp = ',brute_file)
            ext = brute_file.rsplit(sep='.',maxsplit=1)[0]
            cmd = "g++ "+brute_file+" -o "+ext
            with tqdm(total=1.0,desc=brute_file+' compiling',initial=.25) as pbar:
                os.system(cmd)
                pbar.update(.75)
            print()
        if gen_ext == 'cpp':
            # print('cpp = ',gen_file)
            ext = gen_file.rsplit(sep='.',maxsplit=1)[0]
            cmd = "g++ "+gen_file+" -o "+ext
            with tqdm(total=1.0,desc=gen_file+' compiling',initial=.25) as pbar:
                os.system(cmd)
                pbar.update(.75)
            print()
        if test_ext == 'cpp':
            # print('cpp = ',test_file)
            ext = test_file.rsplit(sep='.',maxsplit=1)[0]
            cmd = "g++ "+test_file+" -o "+ext
            with tqdm(total=1.0,desc=test_file+' compiling',initial=.25) as pbar:
                os.system(cmd)
                pbar.update(.75)
            print()
        digit = len(str(no))
        print()
        st = -1.0

        pt='-'*20+test_file+'-'*20
        cprint(pt,'magenta')
        pt = (' '*13+"...Bruteforcing...")
        print()
        cprint(f' # Test File  : ','yellow',end='')
        cprint(f'{test_file}','cyan')
        cprint(f' # Brute File : ','yellow',end='')
        cprint(f'{brute_file}','cyan')
        cprint(f' # Gen File   : ','yellow',end='')
        cprint(f'{gen_file}','cyan')
        cprint(f' # Stress     : ','yellow',end='')
        cprint(f'{no} ','cyan',end=' ')
        if no < 2:
            cprint('time','cyan')
        else :
            cprint('times','cyan')
        print()
        cprint(pt,'blue')
        print()

        for i in range(no):
            pass
            iput = self.cmd_manager(gen_file,'',gen_ext,False)
            # print(iput)
            ans = self.cmd_manager(brute_file,iput,brute_ext,True)
            # print(ans)
            t = time.time()
            result = self.cmd_manager(test_file,iput,test_ext,True)
            # print(ans)
            t = time.time() - t
            cprint('  * '+str(i+1).zfill(digit)+') ','yellow',end='')
            
            # if(iput == '4\n'):
            #     print(ans)
            #     print(result)
            #     break
            if t > st:
                st = t
            if result == ans:
                cprint('Passed...','green',end=' ')
            else :
                cprint('Failed...','red',end=' ')
                cprint(f'[ Time : {t:.4f} sec ]','cyan')
                self.different(iput,result,ans)
                print()
                cprint(' # Failed. :(','red')
                with open('hack.in','w') as f:
                    f.write(iput)
                with open('hack.out','w') as f:
                    f.write(ans)
                
                print()
                cprint('Do you want to add this case to your testcases list? (Y/N) : ','cyan',attrs = ['bold'],end='')
                want = input()
                want.lower()
                if want == 'y' or want =='yes':
                    # cprint('Test case added successfully.','green')
                    self.add_case(iput,ans)
                return
            
            cprint(f'[ Time : {t:.4f} sec ]','cyan')

        print()
        cprint(f' # Slowest : {st:.4f} sec.','blue')
        cprint(f' # Accepted.','green')

        print()
        pt='-'*20+'-'*len(test_file)+'-'*20
        cprint(pt,'magenta')

class Cp_setup:

    def sub_process(self,cmd):
        try:
            x = subprocess.Popen(cmd,stdout=subprocess.PIPE)
            # print('here')
            result = (x.communicate()[0]).decode('utf-8')
        except :
            result = ''
        # print(result)
        return (result)

    def gen_py(self):
        pass
        try :
            cmd = ['python3','-m','tcgen','--path','test']
            result = self.sub_process(cmd)
            # print('result is \n',result)
            if result == '':
                cprint("Can't generated gen file automatically. Sorry sir. :( ",'red')
                return
            with open('gen.py','w') as f:
                f.write(result)
            cprint('gen.py genarated successfully, sir. :D','green')
        except Exception as e:
            print(e)
            cprint("Sorry, Sir can't genarate automatically gen file. ")
    def template(self,file_name='sol.cpp'):
        try :
            # print('Genarating template')
            from settings.compiler import template_path , coder_name
            from system.get_time import digital_time
            
            # print(template_path)
            ext = file_name.rsplit(sep='.',maxsplit=1)
            if(len(ext) == 1) :
                ext = 'cpp'
                file_name = file_name+'.cpp'
            else :
                ext = ext[1]
            
            if ext == 'cpp':
                path = template_path['c++']
            elif ext == 'py':
                path = template_path['python']
            else :
                cprint('File format not supported. Currently only support c++ and python.','red')
            try :
                # path = f"'{path}'"
                # path = 't.cpp'
                if os.path.isfile(file_name):
                    cprint(f"{file_name} already exist, do you want to replace it?(Y/N) :",'cyan',end='')
                    want = input()
                    want = want.lower()
                    if want !='y' and want!='yes':
                        cprint(f"{file_name} creation cancelled.",'red')
                        return
                with open(path,'r') as f:
                    code = f.read()

                code = code.replace('$%CODER%$',coder_name)
                code = code.replace('$%DATE_TIME%$',digital_time())

                with open(file_name,'w') as f:
                    f.write(code)
                # print(code)
                cprint(f'{file_name} created succussfully, sir. :D','green')
            except Exception as e:
                # cprint(e,'red')
                cprint("template path doesn't exist. Sorry sir.",'red')
                cprint("check settings/compiler.py to change your template path :D .",'yellow')
                return
        except Exception as e:
            cprint(e,'red')
            cprint("Can't genarate  template.",'red')
            return 
    def brute(self,file_name='brute.cpp'):
        try :
            if os.path.isfile(file_name):
                cprint(f"{file_name} already exist, do you want to replace it?(Y/N) :",'cyan',end='')
                want = input()
                want = want.lower()
                if want !='y' and want!='yes':
                    cprint(f"{file_name} creation cancelled.",'red')
                    return
            with open(file_name,'w') as f:
                f.write('/* Bruteforce */\n')
            cprint(f'{file_name} created successfully, sir. :D','green')
        except :
            cprint(f"Cant't create {file_name}",'red')

    def setup(self):
        self.template()
        self.brute()
        self.gen_py()
        pass         



class Cp_contest():



    def fetch_problem(self,url = ''):
        try :
            cmd = 'oj-api get-problem ' + url
            cmd = list(cmd.split())

            cp = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            problem = json.loads(cp.stdout)
            # with open('problem.json','w') as f:
            #     f.write(cp.stdout)

            

            if problem['status'] == 'ok':
                # print('ok')
                try :
                    alphabet = problem['result']['context']['alphabet']
                except:
                    alphabet = ''
                problem_name = problem['result']['name']
                problem_name = alphabet + '-'+problem_name
                # print(problem_name)
                if not os.path.isdir(problem_name):
                    os.mkdir(problem_name)
                try:
                    result = f"  * Fetched '{problem_name}'' Successfully"
                    testcases = problem['result']['tests']
                    # print(testcases)
                    # if not os.path.isdir(problem_name):
                    # os.mkdir("'"+problem_name+"'"+'/test')
                    base = os.getcwd()
                    path = os.path.join(base,problem_name,"")

                    info = '{"name" : "$NAME" , "url" : "$URL" }'

                    info = info.replace('$NAME',problem_name)
                    info = info.replace('$URL',url)

                    with open(path+'.info','w') as f:
                        f.write(info)
                    
                    # print(path)
                    if not os.path.isdir(path+"test"):
                        os.mkdir(path+"test")
                    path = os.path.join(path,'test')
                    no = 1
                    for case in testcases:
                        # print(case)
                        fileName_in = 'Sample-'+str(no).zfill(2)+'.in'
                        fileName_out = 'Sample-'+str(no).zfill(2)+'.out'
                        # print(fileName_in)
                        no += 1
                        with open(os.path.join(path,fileName_in),'w') as fin:
                            fin.write(case['input'])
                        with open(os.path.join(path,fileName_out) ,'w') as fout:
                            fout.write(case['output'])
                    cprint(result,'green')

                except Exception as e:
                    print(e)
                
            else :
                result = "Wrong url."
                cprint(result,'result')

            
            
        except Exception as e:
            print('-'*55)
            # print(e)
            cprint("Sorry Can't Fetch.",'red')

    def parse_contest(self,url=''):
        try :

            cprint(' '*17+'...Parsing Contest...'+' '*17,'blue')
            if url == '':
                cprint('Enter the url : ','cyan',end='')
                url = input()
            cprint('-'*55,'magenta')
            # os.system(cmd)
            t = time.time()
            cmd = 'oj-api get-contest ' + url
            cmd = list(cmd.split())

            cp = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            contest = json.loads(cp.stdout)
            # with open('problem.json','w') as f:
            #     f.write(cp.stdout)

            result = "\tFetched Contest info..."
            if contest['status'] == 'ok':
                cprint(result,'green')
            else :
                cprint("Sorry contest can't be fetched. Sorry sir. :( ",'red')
                return
            # print(contest)
            path = os.getcwd()
            # print(path)
            contest_name = contest['result']['name']
            cprint(f' # Contest name : {contest_name}','green')

            if not os.path.isdir(contest_name):
                os.mkdir(contest_name)
                # cprint('Contest folder created.','green')


            print()
            os.chdir(os.path.join(path,contest_name))
            # print(os.getcwd())
            problem = contest['result']['problems']
            with open('t.json','w') as f:
                f.write(str(contest))

            for key in problem:
                url = key['url']
                # print(url)
                # Cp_Problem.fetch_problem(url)
                self.fetch_problem(url=url)

            os.chdir(path)
            # print(os.getcwd())
            print()
            cprint(" # Done. :D",'green')
            cprint(f" # Time taken {time.time()-t:.4f} sec.",'blue')
            cprint('-'*55,'magenta')
        
        except Exception as e:
            cprint(e,'red')




def cp_manager(msg):
    
    if 'parse' in msg:
        obj = Cp_Problem()
        obj.fetch_problem()
    elif 'submit' in msg:
        msg = msg.replace('submit','')
        msg = msg.replace(' ','')
        obj = Cp_Submit()
        obj.find_files(msg)
    elif '-t' in msg or 'template' in msg:
        msg = msg.replace('-t','')
        msg = msg.replace('template','')
        msg = msg.split()

        if (len(msg)) == 0:
            msg = 'sol.cpp'
        else :
            msg = msg[0]

        obj = Cp_setup()
        obj.template(file_name=msg)
    
    elif 'contest' in msg:
        obj = Cp_contest()
        obj.parse_contest()

    elif 'login' in msg:
        obj = Cp_login()
        obj.login()
    elif 'add' in msg:
        obj = Cp_add_test()
        obj.add_case()
    elif 'test -oj' in msg:
        msg = msg.replace('test -oj','')
        msg = msg.replace(' ','')
        obj = Cp_Test()
        obj.find_files(msg)
    elif 'test' in msg:
        msg = msg.replace('test','')
        msg = msg.replace(' ','')
        obj = Cp_my_tester()
        # obj.TLE = 1
        obj.find_files(msg)
    elif 'setup' in msg:
        obj = Cp_setup()
        obj.setup()
    elif 'brute' in msg:
        obj = Cp_bruteforce()
        obj.run()
    elif 'gen' in msg:
        obj = Cp_setup()
        obj.gen_py()
    else :
        cprint('Arguments Error','red')

def if_cp_type(msg):
    # print(msg)
    for key in cp_keys:
        if key in msg:
            msg = msg.replace(key,'')
            cp_manager(msg.lower())
            return True 
    return False



if __name__ == "__main__":
    # obj = Cp_Problem()
    # Cp_Problem.fetch_problem()
    # obj = Cp_Submit()
    # obj.find_files()
    # Cp_login.login()
    obj = Cp_add_test()
    obj.add_case()
    # obj = Cp_Test()
    # obj.find_files()
    # cprint("Enter something for testing purpose : ",'cyan',end='')
    # x = input()
    # cprint(x,'blue')
