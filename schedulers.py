from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates


class FCFS(SchedulerDES):
    '''
    Implementation of FCFS/FIFO scheduling algorithms
    using OOP techniques
    '''

    def scheduler_func(self, cur_event):
        '''
        Parameters: Event object
        Schedules next process to be executed
        Returns: Process object with least arrival time
        '''
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_proc):
        '''
        Parameters: Process object
        Runs current process and prepares the next event
        Returns: Event object
        '''
        cur_proc.process_state = ProcessStates.RUNNING
        cur_proc.run_for(cur_proc.service_time, self.time)
        cur_proc.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_proc.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time + cur_proc.service_time)


class SJF(SchedulerDES):
    '''
    Implementation of Shortest Job First scheduling algorithm
    using OOP techniques
    '''

    def scheduler_func(self, cur_event):
        '''
        Parameters: Event object
        Schedules next process to be run
        Returns: Process object
        '''
        cur_proc = None
        for p in self.processes:
            if (p.process_state == ProcessStates.READY and cur_proc is None):
                cur_proc = p
            elif (p.process_state == ProcessStates.READY) and (p.service_time < cur_proc.service_time):
                cur_proc = p
        return cur_proc

    def dispatcher_func(self, cur_proc):
        '''
        Parameters: Event object
        Runs current process and prepares the next event
        Returns: Event Object
        '''
        cur_proc.process_state = ProcessStates.RUNNING
        cur_proc.run_for(cur_proc.service_time, self.time)
        cur_proc.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_proc.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time + cur_proc.service_time)


class RR(SchedulerDES):
    '''
    Implementation of Round Robin scheduling algorithm
    using OOP techniques
    '''
    # arbitary value to loop through process queue
    proc_index = 0

    def scheduler_func(self, cur_event):
        '''
        Parameters: Event object
        Schedules next process to be run
        Returns: Process object
        '''
        try:
            while self.processes[self.proc_index].process_state != ProcessStates.READY:
                self.proc_index += 1
            return self.processes[cur_event.process_id]
        except IndexError:
            self.proc_index = 0
            return self.scheduler_func(cur_event)

    def dispatcher_func(self, cur_proc):
        '''
        Parameters: Event object
        Runs current process and prepares the next event
        Returns: Event Object
        '''
        quantum = self.quantum
        cur_proc.process_state = ProcessStates.RUNNING
        if quantum < cur_proc.remaining_time:
            cur_proc.run_for(quantum, self.time)
            cur_proc.process_state = ProcessStates.READY
            return Event(process_id=cur_proc.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=self.time + quantum)
        else:
            rem_time = cur_proc.remaining_time
            cur_proc.run_for(cur_proc.remaining_time, self.time)
            cur_proc.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_proc.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time + rem_time)


class SRTF(SchedulerDES):
    '''
    Implementation of Round Robin scheduling algorithm
    using OOP techniques
    '''

    def scheduler_func(self, cur_event):
        '''
        Parameters: Event object
        Schedules next process to be run
        Returns: Process object
        '''
        cur_proc = None
        for p in self.processes:
            if p.process_state == ProcessStates.READY and cur_proc is None:
                cur_proc = p
            elif p.process_state == ProcessStates.READY and p.remaining_time < cur_proc.remaining_time:
                cur_proc = p
        return cur_proc

    def dispatcher_func(self, cur_proc):
        '''
        Parameters: Event object
        Runs current process and prepares the next event
        Returns: Event Object
        '''
        quantum = 1 / self._arrivals_per_time_unit
        cur_proc.process_state = ProcessStates.RUNNING
        if quantum < cur_proc.remaining_time:
            cur_proc.run_for(quantum, self.time)
            cur_proc.process_state = ProcessStates.READY
            return Event(process_id=cur_proc.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=self.time + quantum)
        else:
            rem_time = cur_proc.remaining_time
            cur_proc.run_for(cur_proc.remaining_time, self.time)
            cur_proc.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_proc.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time + rem_time)
