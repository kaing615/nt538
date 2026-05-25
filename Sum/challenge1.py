import multiprocessing

def worker_task(args):
    file_path, start_byte, end_byte = args
    total = 0
    
    with open(file_path, 'r') as f:
        f.seek(start_byte)
        chunk = f.read(end_byte - start_byte)
        
        for s in chunk.split():
            try:
                val = float(s)
                if val > 0 and val.is_integer():
                    ival = int(val)
                    if ival % 3 == 0:
                        total += ival
            except ValueError:
                continue
                
    return total


def MAIN(input_file_path):
    with open(input_file_path, "r") as f:
        line1 = f.readline()
        if not line1: 
            return 0
        n = int(line1.strip())
        if n == 0: 
            return 0
            
        data_start_pos = f.tell()
        f.seek(0, 2)
        file_size = f.tell()
        
    data_size = file_size - data_start_pos
    num_proc = 16
    chunk_size = data_size // num_proc
    
    tasks = []
    current_start = data_start_pos
    
    with open(input_file_path, "r") as f:
        for i in range(1, num_proc):
            target_end = data_start_pos + i * chunk_size
            f.seek(target_end)
            
            while True:
                char = f.read(1)
                if not char or char.isspace():
                    break
            
            current_end = f.tell()
            tasks.append((input_file_path, current_start, current_end))
            current_start = current_end
            
        tasks.append((input_file_path, current_start, file_size))
        
    with multiprocessing.Pool(processes=num_proc) as pool:
        results = pool.map(worker_task, tasks)
        
    return sum(results)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python challenge1.py <input_file_path>")
    sys.exit(1)

    input_file_path = sys.argv[1]
    result = MAIN(input_file_path)
    print(result)
