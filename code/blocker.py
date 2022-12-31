import os
import datetime
import re

class Blocker:
    
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
    WEBSITES_PATH = r"C:\Users\matth\OneDrive\Bureaublad\python\WebsiteBlocker\websites.txt"

    def __init__(self) -> None:
        self.blocked_websites: list = self.blocked_website_retriever()
        self.redirection = "0.0.0.0"
    
    def blocked_website_retriever(self):
        """Opens the website.txt file and adds the blocked websites to list."""

        blocked_website_list = []
        
        # To avoid an error, if the file does not exist yet, it will first be created
        if os.path.exists(self.WEBSITES_PATH) == False:
            with open(self.WEBSITES_PATH,"w") as file:
                pass

        with open(self.WEBSITES_PATH,'r+') as file:            
            
            lines = file.readlines()

            for line in lines:
                try:
                    website, redirected, date, time = line.split()
                    blocked_website_list.append([website,redirected,date,time])
                
                except ValueError:
                    if line == "\n":
                        continue
                except:
                    print("There seems to be a problem with the unpacking in the 'Blocker.blocked_website_retriever' function")

            return blocked_website_list

    
    def block_website(self,website:str) -> tuple:
        """add websites to hosts file and to the webstites.txt file"""
        
        date = datetime.datetime.now()
        
        # If already in file
        if f"www.{website}" in [i[0] for i in self.blocked_websites]:
            self.blocked_websites.append(["Already in","Already in","Already in"])
            return ["Already in","Already in","Already in"]
        
        elif website == "":
            self.blocked_websites.append(["Empty","Empty","Empty"])
            return ["Empty","Empty","Empty"]
        
        with open(self.WEBSITES_PATH, "a") as file:
            file.write(f"www.{website} {self.redirection} {date}\n")


        # Else add the website to the Hosts file, once with and once without "www"
        with open(self.HOSTS_PATH,"a") as hosts:

            hosts.write(f"{self.redirection} {website}\n")
            hosts.write(f"{self.redirection} www.{website}\n")
        
        #Temporarly add it to list, until the new program restarts
        self.blocked_websites.append([f"www.{website}",self.redirection])
        
        return f"www.{website}",self.redirection,date

   
    def unblock_website(self,website:str,index=int) -> None:
        """Removes website from both the Hosts file and the websites.txt file"""
        self.blocked_websites.pop(index)
        with open(self.WEBSITES_PATH,'r') as file:
            file_lines = file.readlines()

        with open(self.WEBSITES_PATH,'w') as file_writerover:
            for line in file_lines:
                if website in line:
                    continue
                
                file_writerover.write(line)


        with open(self.HOSTS_PATH,"r") as file_content:
            hosts_full_content = file_content.readlines()

        with open(self.HOSTS_PATH,"w") as hosts:
            for line in hosts_full_content:
                
                if line[0] == "#" or line == "\n":
                    hosts.write(line)
                    
                else:
                    if website in line.split()[1]:
                        continue
                    
                    hosts.write(line)
  
    def resetter(self):
        """resetting both the hosts file and the websites.txt file"""

        print("resetting object")
        #only keeps the \n and commented out lines
        with open(self.HOSTS_PATH,"r") as file_content:
             hosts_full_content = file_content.readlines()

        with open(self.HOSTS_PATH,"w") as hosts:
            for line in hosts_full_content:
                if line[0] == "#" or line == "\n":
                    hosts.write(line)

        #just fully empties the file
        with open(self.WEBSITES_PATH,'w') as file_writerover:
            pass
        
        self.blocked_websites = []




def url_cleaner_validater(url:str) -> str:
    """Returns the url without the www or https://"""
    url = url.lower()
    url = "".join(url.split())

    if url.startswith("www."):
        url = re.sub("www.","",url)
    
    elif url.startswith("https://www.") or url.startswith("https://"):
        url = re.sub("https://www.","",url)
        url = re.sub("https://","",url)

    return url


if __name__ == "__main__":

    print("This is the blocker.py file")
