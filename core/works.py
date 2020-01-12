from time import sleep
from core import fight
from ai import AI

class Work:
    NULL = None
    def routine(self):
        raise Exception
    def process(self):
        args = self.routine()
        args.extend([Work.NULL]*(3-len(args)))
        return args

class Send(Work):
    def __init__(self, arg0, arg1, arg2):
        self.name, self.lang, self.code = arg0, arg1, arg2
    def routine(self):
        if AI.exist(self.name):
            return [1, 'AI, {}, already exist'.format(self.name)]
        ai = AI('Default', self.name, self.lang)

        exitCode, logs = ai.write(self.code)
        if exitCode != 0:
            return [exitCode, logs]

        exitCode, logs = ai.compile()
        print('Compile', self.name, self.lang)
        return [exitCode, logs]

class Set(Work):
    def __init__(self, arg0, arg1, arg2):
        self.name = arg0
    def routine(self):
        if not AI.exist(self.name):
            return [1, 'AI, {}, doesn\'t exist'.format(self.name)]

        exitCode, logs = 0, ''
        sleep(2)
        print('Set', self.fileName)
        return [exitCode, logs]

class Fight(Work):
    def __init__(self, arg0, arg1, arg2):
        self.name1, self.name2 = arg0, arg1
    def routine(self):
        if not AI.exist(self.name1):
            return [-1, 'AI1, {}, doesn\'t exist'.format(self.name1)]
        if not AI.exist(self.name2):
            return [-1, 'AI2, {}, doesn\'t exist'.format(self.name2)]

        ai1 = AI.get(self.name1)
        ai2 = AI.get(self.name2)
        game, ai1, ai2 = fight(ai1, ai2)

        result = game.winner
        log1 = ''.join(ai1.logHistory)
        log2 = ''.join(ai2.logHistory)
        print('Fight', self.name1, self.name2)
        return [result, log1, log2]

workList = [Send, Set, Fight]
def work(line):
    requestId, workId, arg0, arg1, arg2, status = line
    return workList[workId](arg0, arg1, arg2)
