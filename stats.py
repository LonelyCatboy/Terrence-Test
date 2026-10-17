import requests

api_key = "lksdfjsdklböjnkäsdl#WSEPFJO"
#api_key = "67"

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


class StatsDB():
    def __init__(self):
        self.url = "https://terrencetestserver.serveousercontent.com"

    #Load Stats from Database
    def load_stats(self):
        req = {
            "KEY": api_key
        }

        try:
            response = requests.post(f"{self.url}/leaderboard/*",json=req)
        except Exception as e:
            print(f"Error: {e}")
            return ["Error: Could not connect to server"]

        
        print(response.json())
        if response.json()["success"] == False:
            print(response.json())
            return response.json()["message"]
        
        stats = response.json()["leaderboard"]

        for i in range(len(stats)):
            stats[i] = f"{stats[i][0]}: {stats[i][1]} Jeph\n"
        
        return stats

    def save_stats(self, name, score):
        req = {
                    "KEY": api_key,
                    "username": name,
                    "score": score
                }
        try:
            response = requests.post(f"{self.url}/save_score", json=req)

            if response.json()["success"]:
                return ["Score saved successfully"]

            
        except Exception as e:
            print(f"Error: {e}")
            return ["Error: Could not connect to server"]


def testvalues():
    stats = StatsDB()
    for i in range(100):
        stats.save_stats(f"Test{i}", i)

def updatevalue(UserNum, num):
    stats = StatsDB()
    stats.save_stats(f"Test{UserNum}", num)

if __name__ == "__main__":
    updatevalue(67, 1000)

    