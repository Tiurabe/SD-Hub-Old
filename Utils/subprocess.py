class Process:
    # aria_mode: Shows progress bar for aria2c downloads (experimental)

    def __init__(self, raw_command: str, aria_mode=None):
        self.command = raw_command
        self.process = None
        self.output = []
        self.return_code = None
        self.mode = aria_mode
        self.status = "Awaiting"

    def run(self):
        try:
            self.status = "Running"
            command = shlex.split(self.command)
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            if self.mode is True:
                aria_finished = False
                while True:
                    line = self.process.stdout.readline()
                    if line == '' and not self.is_alive():
                        break
                    if 'Download Results' in line:
                        print("\n")
                        print(line, end='')
                        aria_finished = True
                    else:
                        match = re.search(r'\[[^\]]+\]', line)
                        if match:
                            stripped_line = match.group().strip()
                            print("\r", end='')
                            print(f"\r{stripped_line}", end='')
                        else:
                            print(line, end="")
                            print("im here!")
        except (OSError, ValueError, subprocess.CalledProcessError, re.error) as e:
            print(f"Error running command: {e}")
            self.status = "Error"

    def wait(self):
        stdout, stderr = self.process.communicate()
        self.output = stdout.splitlines()
        self.return_code = self.process.returncode
        print(stderr)
        self.status = "Process finished running"

    def is_alive(self):
        return self.process.poll() is None

    def kill(self):
        self.process.kill()
        self.status = "Process Killed"

    def __str__(self):
        return f'Process(command={self.command}, mode={self.mode}, returncode={self.return_code}, output={self.output})'
