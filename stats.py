class StatsFile():

    def __init__(self):
        return

    #Load Stats from File
    def load_stats(self):
            try:
                with open("stats.txt", "r") as f:
                    stats = f.readlines()
                stats = [s.strip() for s in stats]
                stats.sort(key=lambda x: float(x.split(":")[1]), reverse=True)
                stats = [f"{s} Jeph\n" for i,s in enumerate(stats)]
                return stats
            except FileNotFoundError:
                return []


    #Save Stats to File
    def save_stats(self, name, score):
        with open("stats.txt", "a") as f:
            f.write(f"{name}:{score}\n")