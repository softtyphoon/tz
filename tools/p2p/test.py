import multiprocessing
import time

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                # print ('%s: Exiting' % proc_name)
                # self.task_queue.task_done()
                break
            print ('%s: %s' % (proc_name, next_task))
            answer = next_task() # __call__()
            fn = '%s.txt' % (next_task)
            a = open(fn, 'w+')
            a.close()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self):
        time.sleep(0.1) # pretend to take some time to do the work
        return '%s * %s = %s' % (self.a, self.b, self.a * self.b)
    def __str__(self):
        return '%s%s' % (self.a, self.b)


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count()
    num_consumers = 4
    print ('Creating %d consumers' % num_consumers)
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 2
    # for i in range(num_jobs):
        # tasks.put(Task(i, i))
        # tasks.put(None)
    tasks.put(Task(0, 0))
    tasks.put(Task(1, 1))

    # Add a poison pill for each consumer
    # for i in range(num_consumers):
        # tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    num =0
    while True:
        print num
        result = results.get()
        print result
        num = num + 1
        if num == num_jobs:
            break
    print '--------------------------'
    tasks.put(Task(0, 2))
    tasks.put(Task(1, 3))
    tasks.put(Task(1, 4))
    tasks.join()
    time.sleep(10)
    for i in range(num_consumers):
        tasks.put(None)
    while True:
        # print num
        result = results.get()
        # print result
        num = num + 1
        if num == 3:
            break
    # while num_jobs:
        # result = results.get()
        # print ('Result:', result)
        # num_jobs -= 1