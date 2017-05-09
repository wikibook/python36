import sqlite3
import sys
import re

# 데이터베이스 경로 설정
if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = ":memory:"

con = sqlite3.connect(path)
con.isolation_level = None
cur = con.cursor()

buffer = ""

def PrintIntro():
    "프로그램 소개 메시지"
    print("pysqlite의 command 프로그램입니다.")
    print("특수 명령어를 알고 싶으시면 '.help;'를 입력하세요.")
    print("SQL 구문은 ';'으로 끝나야 합니다.")

def PrintHelp():
    "도움말"
    print(".dump\t\t데이터베이스의 내용을 덤프합니다.")

def SQLDump(con, file=None):
    "데이터베이스 내용 덤프"
    if file != None:
        f = open(file, "w")
    else:
        f = sys.stdout

    for l in con.iterdump():
        f.write("{0}\n".format(l))

    if f != sys.stdout:
        f.close()

PrintIntro()

while True:
    line = input("pysqlite>> ")
    if buffer == "" and line == "":
        break
    buffer += line

    if sqlite3.complete_statement(buffer):
        buffer = buffer.strip()

        if buffer[0]==".":
            cmd = re.sub('[ ;]', ' ', buffer).split()
            if cmd[0] == '.help':
                PrintHelp()
            elif cmd[0] == '.dump':
                if len(cmd) == 2:
                    SQLDump(con, cmd[1])
                else:
                    SQLDump(con)
        else:
            try:
                buffer = buffer.strip()
                cur.execute(buffer)

                if buffer.lstrip().upper().startswith("SELECT"):
                    print(cur.fetchall())
            except sqlite3.Error as e:
                print("Error: ", e.args[0])
            else:
                print("구문이 성공적으로 수행되었습니다.")
        buffer=""
con.close()
print("프로그램을 종료합니다. 야옹~")