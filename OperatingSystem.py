cpu_ticks = 0

def cputicks(num = 1):
    global cpu_ticks
    if num == 0:
        return cpu_ticks
    else:
        cpu_ticks += 1
        return cpu_ticks
        

class Process:
    def __init__(self, pid, instructions, memory_required):
        self.pid = pid                       # Process ID
        self.instructions = instructions      # List of instructions
        self.memory_required = memory_required # Memory required
        self.current_instruction = 0          # Pointer to the current instruction
        self.state = 'READY'                  # Process state: READY, WAITING, TERMINATED
        self.cpu_time = 0                     # Time spent on CPU
   
    def get_next_instruction(self):
        """Get the next instruction, or None if done."""
        if self.current_instruction <= len(self.instructions):
            return self.instructions[self.current_instruction]
        else:
            self.state = 'TERMINATED'
            return None

    def execute_instruction(self):
        """Simulates execution of the current instruction."""
        instruction = self.get_next_instruction()
        if instruction == 'COMPUTE':
            self.cpu_time += 5  # COMPUTE takes 5 ticks
            self.current_instruction += 1

            for i in range(5):
                cputicks()

            return (5,"COMPUTE")  # Returns CPU ticks used
        elif instruction == 'INPUT':
            self.cpu_time += 1  # INPUT takes 1 tick, then waits
            self.current_instruction += 1
            self.state = 'WAITING'

            cputicks()

            return (1,"OUTPUT")  # Returns CPU ticks used
        elif instruction == 'OUTPUT':
            self.cpu_time += 1  # OUTPUT takes 1 tick, then waits
            self.current_instruction += 1
            self.state = 'WAITING'

            cputicks()

            return (1,"INPUT")  # Returns CPU ticks used
        return 0  # No instruction (TERMINATED)

class MemoryManager:
    def __init__(self, os_memory_reserved, user_memory, allocation_strategy='first_fit', max_processes=10):
        self.os_memory_reserved = os_memory_reserved  # Memory reserved for the OS
        self.allocation_strategy = allocation_strategy
        self.max_processes = max_processes
        self.user_memory = user_memory
        self.free_memory = user_memory  # Total free memory
        self.free_blocks = [(os_memory_reserved, user_memory)]
        self.allocated_memory = {0: (0, os_memory_reserved)}
        self.allocation_pointer = os_memory_reserved  # Next allocation pointer
    
    def allocate_memory(self, process):
        """Allocates memory to a process."""
        print("\n")
        print(len(self.allocated_memory))
        print(self.allocation_strategy)
        if len(self.allocated_memory)  >= self.max_processes:
            print(f"Process {process.pid} failed to allocate memory. Maximum number of processes reached.")
            return False

        else:
            size = process.memory_required    
            if self.allocation_strategy == 'first_fit':
                for i, (start, block_size) in enumerate(self.free_blocks):
                    if size <= block_size:
                        print("block_size " + str(block_size))
                        print("size " + str(size))
                        self.allocated_memory[process.pid] = (start, size)
                        print(f"Process {process.pid} allocated {size} units of memory and starts at {start}.")
                        print(self.allocated_memory)
                        if size == block_size:
                            self.free_blocks.pop(i)
                        else:
                            self.free_blocks[i] = (start + size, block_size - size)
                        print(f"Process {process.pid} allocated {size} units of memory.")
                        return True
                print(f"Process {process.pid} failed to allocate {size} units of memory.")
                return False
            # elif self.allocation_strategy == 'best_fit':
            #     if len(self.allocated_memory) >= self.max_processes:
            #         print(f"Process {process.pid} failed to allocate memory. Maximum number of processes reached.")
            #         return False

            #     size = process.memory_required
            #     best_fit = None
            #     for i, (start, block_size) in enumerate(self.free_blocks):
            #         if size <= block_size and (best_fit is None or block_size < best_fit[1]):
            #             best_fit = (i, start, block_size)
            #     if best_fit is not None:
            #         i, start, block_size = best_fit
            #         self.allocated_memory[process.pid] = (start, size)
            #         if size == block_size:
            #             self.free_blocks.pop(i)
            #         else:
            #             self.free_blocks[i] = (start + size, block_size - size)
            #         print(f"Process {process.pid} allocated {size} units of memory.")
            #         return True
            #     print(f"Process {process.pid} failed to allocate {size} units of memory.")
            #     return False

    def release_memory(self, process):
        """Releases memory for a terminated process."""
        if process.pid in self.allocated_memory:
            start, size = self.allocated_memory.pop(process.pid)
            self.free_blocks.append((start, size))
            self.free_blocks.sort()  # Ensure memory is sorted by address
            print(f"Process {process.pid} released {size} units of memory.")

class RoundRobinScheduler:
    def __init__(self, quantum, context_switch=1):
        self.quantum = quantum  # Time slice for each process
        self.ready_queue = []   # Queue of processes ready to run
        self.event_manager = EventManager()
        self.context_switch = context_switch
        # self.waiting_processes = {1: [], 2: []}  # Processes waiting for INPUT (1) or OUTPUT (2)
        self.waiting_processes = ()
       


    def add_process(self, process):
        """Add a process to the ready queue."""
        self.ready_queue.append(process)

    

    def schedule_for_ticks(self, ticks_to_run):
        """Run processes up to the given number of ticks, respecting the quantum."""
        total_ticks_used = 0
        waiting_processes = []

        # while self.waiting_processes[1] or self.waiting_processes[2]:
        #     for process, event_time in self.waiting_processes[1]:
        #         if event_time <= cpu_ticks:
        #             self.event_manager.trigger_event(event_number)
        #             self.waiting_processes[1].remove((process, event_time))
        #     for process, event_time in self.waiting_processes[2]:
        #         if event_time <= cpu_ticks:
        #             self.event_manager.trigger_event(event_number)
        #             self.waiting_processes[2].remove((process, event_time))
        
        while self.ready_queue and total_ticks_used < ticks_to_run:
            current_process = self.ready_queue.pop(0)
            print(f"\nScheduling Process {current_process.pid}")
            time_slice = 0
            while time_slice <= self.quantum and current_process.state == 'READY':

                current_process
                ticks_used = current_process.execute_instruction()
                time_slice += ticks_used[0]
                total_ticks_used += ticks_used[0]

               
                if current_process.state == 'WAITING':
                    print(f"Process {current_process.pid} is waiting.")
                    if ticks_used[1] == 'INPUT':
                     
                        waiting_processes.append([0,current_process, cputicks(0) + 8])

                    if ticks_used[1] == 'OUTPUT':
                
                        waiting_processes.append([1,current_process, cputicks(0) + 5])   
                    break
                
                if current_process.state == 'TERMINATED':
                    print(f"Process {current_process.pid} terminated.")
                    break

                if total_ticks_used >= ticks_to_run:  # Stop if tick limit is reached
                    break

            if current_process.state == 'READY':
                for i in range(self.context_switch):
                    cputicks()
                self.ready_queue.append(current_process)  # Re-add to queue if not done

        return (total_ticks_used, waiting_processes)

class EventManager:
    def __init__(self):
        # self.waiting_processes = {1: [], 2: []}  # Processes waiting for INPUT (1) or OUTPUT (2)
        self.waiting_processes = [[],[]]
        self.event_number = 0
        self.event_triggered = False
    


    def wait_for_event(self, process, event_number):
        self.waiting_processes[event_number].append(process)
        print(f"Process {process.pid} is waiting for event {event_number}")

    def check_events(self):
        """Check if any processes are waiting for an event."""
        for processes in self.waiting_processes:
            for process in processes:
                if process[0] >= cputicks(0):
                    self.trigger_event(event_number)
                    print(f"Event {event_number} is pending.")
                    self.event_triggered = True
                    self.event_number = event_number
            self.event_triggered = False

    def trigger_event(self, event_number):
        """Triggers the event, allowing waiting processes to resume."""
        if event_number == 1:
            self.waiting_processes[event_number][0].state = 'READY'
            process = self.waiting_processes[event_number][0]
            self.waiting_processes[event_number].pop(0)
            self.scheduler.add_process(process)

            print(f"Event {event_number} triggered. Process {process.pid} is now ready.")
         
            
        if event_number == 2:
            self.waiting_processes[event_number][0].state = 'READY'
            process = self.waiting_processes[event_number][0]
            self.waiting_processes[event_number].pop(0)
            self.scheduler.add_process(process)


            print(f"Event {event_number} triggered. Process {process.pid} is now ready.")

class Simulator:
    def __init__(self, quantum, reserved_memory, user_memory, max_processes, mem_alloc, context_switch):
        self.scheduler = RoundRobinScheduler(quantum, context_switch)
        self.memory_manager = MemoryManager(reserved_memory, user_memory, mem_alloc, max_processes)
        self.event_manager = EventManager()
        self.context_switch = context_switch
        self.total_process_size = 0

    def add_process(self, pid, instructions, memory_required):
        """Add a process to the simulation."""
        process = Process(pid, instructions, memory_required)
        if self.memory_manager.allocate_memory(process):
            self.scheduler.add_process(process)
            self.total_process_size += memory_required
    
    # def remove_process(self, process):
    #     """Remove a process from the simulation."""
    #     self.scheduler.remove_process(process)
    #     self.memory_manager.release_memory(process)

    # def show_stats(self):
    #     """Display current stats about the processes and memory."""
    #     active_processes = sum(1 for p in self.scheduler.ready_queue if p.state == 'READY')
    #     waiting_processes = sum(1 for p in self.scheduler.ready_queue if p.state == 'WAITING')
    #     terminated_processes = sum(1 for p in self.scheduler.ready_queue if p.state == 'TERMINATED')
    #     total_processes = len(self.scheduler.ready_queue)
        
    #     print("\n--- SYSTEM STATS ---")
    #     print(f"Total Processes: {total_processes}")
    #     print(f"Active (READY) Processes: {active_processes}")
    #     print(f"Waiting Processes: {waiting_processes}")
    #     print(f"Terminated Processes: {terminated_processes}")

    # def user_input_pause(self):
    #     """Pause the simulation and wait for user input to continue or stop."""
    #     choice = input("\nPick from OPTIONS \nShow Jobs \nShow Queues \nShow Memory").strip().lower()
    #     match choice:
    #         case 'show jobs':
    #             print("\n--- JOBS ---")
    #             for process in self.scheduler.ready_queue:
    #                 print(f"Process {process.pid}: {process.state}")
    #         case 'show queues':
    #             print("\n--- QUEUES ---")
    #             print("Ready Queue:", [p.pid for p in self.scheduler.ready_queue if p.state == 'READY'])
    #             print("Waiting Queue:", [p.pid for p in self.scheduler.ready_queue if p.state == 'WAITING'])
    #         case 'show memory':
    #             print("\n--- MEMORY ---")
    #             print("Free Blocks:", self.memory_manager.free_blocks)
    #             print("Allocated Memory:", self.memory_manager.allocated_memory)
    #         case _:
    #             print("Invalid choice. Please enter a valid option.")
    #     return choice == 'yes'  # Return True if user wants to continue

    def get_ticks_from_user(self):
        """Ask the user for the number of ticks to run the simulation."""
        while True:
            try:
                ticks = int(input("\nEnter the number of ticks to run the simulation (must be greater than 5): "))
                while ticks < 5:
                    print("Please enter a number greater than 5.")
                    ticks = int(input("\nEnter the number of ticks to run the simulation: "))


                return ticks
            except ValueError:
                print("Invalid input. Please enter a valid number of ticks.")

    def run(self):
        """Run the simulator."""

        continue_simulation = True
        while continue_simulation:
            ticks_to_run = self.get_ticks_from_user()  # Get how many ticks to run
            total_ticks = 0

            global cpu_ticks
            while total_ticks <= ticks_to_run:
                    processing = self.scheduler.schedule_for_ticks(ticks_to_run - total_ticks)
                    used_ticks = processing[0]
                    wait_processes = processing[1]

                    if wait_processes:
                        for i in range(len(wait_processes)):
                          
                            self.event_manager.waiting_processes[wait_processes[i][0]].append([wait_processes[i][2], wait_processes[i][1]])
                           
                   
                    self.event_manager.check_events()
                    
                    total_ticks += used_ticks
                    if used_ticks == 0:  # If no more ticks are being used (all processes done)
                        break

        self.scheduler.schedule()
        # Release memory for all terminated processes
        for process in self.scheduler.ready_queue:
            if process.state == 'TERMINATED':
                self.memory_manager.release_memory(process)




def main():

   

    while True:
        try:
            s = int(input("Enter the amount of RAM reserved for the OS  (For example 128): "))
            if s < 100:
                print("Please enter a valid amount of RAM reserved for the OS (For example 128).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            u = int(input("Enter memory available for processes (For example 1024): "))
            if u < 100:
                print("Please enter a valid amount of memory available for processes (For example 1024).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            n = int(input("Enter the MAX amount of processes: ")) 
            n = n + 1
            if n < 1:
                print("Please enter a valid amount of processes (at least 1).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            context_switch = int(input("Enter the context switch time (For example 1): "))
            if context_switch < 1:
                print("Please enter a valid context switch time (at least 1).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            x = int(input("Enter the number of ticks (For example 5): "))
            if x < 1:
                print("Please enter a valid number of ticks (at least 1).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


    mem_alloc = ' '
    mem_alloc = input("Enter memory allocation method (F for first fit, B for best fit or N for next fit): ")
    mem_alloc = mem_alloc.upper()
    if mem_alloc not in ['F', 'B', 'N']:
        print("Incorrect input for memory allocation method. Therefore, the default method (First Fit) will be used.")
        mem_alloc = 'F' 
    mem_alloc = mem_alloc.upper()
    
    if mem_alloc == 'F' :
        mem_alloc = 'first_fit'
    elif mem_alloc == 'B':
        mem_alloc = 'best_fit'
    elif mem_alloc == 'N':
        mem_alloc = 'next_fit'
        
    simulator = Simulator(x, s, u, n, mem_alloc, context_switch)
    
    # Create and add processes (pid, instructions, memory_required)
    simulator.add_process(1, ["INPUT", "COMPUTE", "COMPUTE"], 64)
    simulator.add_process(2, ["INPUT", "COMPUTE", "OUTPUT", "COMPUTE"], 128)
    simulator.add_process(3, ["COMPUTE", "COMPUTE", "COMPUTE", "OUTPUT"], 512)
    simulator.add_process(4, ["OUTPUT", "OUTPUT", "OUTPUT"], 256)
    simulator.add_process(5, ["COMPUTE", "COMPUTE", "COMPUTE"], 128)
    simulator.add_process(6, ["COMPUTE", "COMPUTE", "COMPUTE"], 64)
    simulator.add_process(7, ["COMPUTE", "COMPUTE", "COMPUTE"], 128)
    
    # Run the simulation
    simulator.run()

if __name__ == "__main__":
    main()
