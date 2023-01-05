import os
import datetime
import re
import json


class Blocker:
    
    path_hosts = r"C:\Windows\System32\drivers\etc\hosts"
    path_website = r".\save_files\blocked_website_list.txt"

    def __init__(self) -> None:
        self.blocked_websites = self.blocked_website_retriever()
        self.redirection = "0.0.0.0"
    
    def blocked_website_retriever(self):
        """Opens the txt file and adds the blocked websites to a list."""

        blocked_website_list = []
        
        # To avoid an error, if the file does not exist yet, it will first be created
        if not os.path.exists(self.path_website):
            with open(self.path_website,"w") as file:
                pass

        with open(self.path_website,'r+') as file:            
            lines = file.readlines()

            for line in lines:
                try:
                    website, redirected, date, time = line.split()
                    blocked_website_list.append([website,redirected,date,time])
                
                except ValueError:
                    if line == "\n":
                        continue
                except:
                    raise "There seems to be a problem with the unpacking in the 'Blocker.blocked_website_retriever' method"

            return blocked_website_list

    
    def block_website(self,website:str) -> tuple:
        """Adds websites to hosts file and to the blocked_website_list.txt file"""
        
        date = datetime.datetime.now()
        website = url_cleaner_validater(website)

        #if it is empty or already exist
        if f"www.{website}" in [i[0] for i in self.blocked_websites]:
            self.blocked_websites.append(["Already in","Already in","Already in"])
            return ["Already in","Already in","Already in"]
        
        elif website == "":
            self.blocked_websites.append(["Empty","Empty","Empty"])
            return ["Empty","Empty","Empty"]
        
        # Else add the website to the Hosts file, once with and once without "www."
        with open(self.path_website, "a") as file:
            file.write(f"www.{website} {self.redirection} {date}\n")

        with open(self.path_hosts,"a") as hosts:

            hosts.write(f"{self.redirection} {website}\n")
            hosts.write(f"{self.redirection} www.{website}\n")
        
        #Temporarly add it to list, until the new program restarts
        self.blocked_websites.append([f"www.{website}",self.redirection])
        
        return f"www.{website}",self.redirection,date
    
    def block_list_website(self,list_websites:list) -> list:
        date = datetime.datetime.now()
        return_list = []
        
        for website in list_websites:
            
            cleaned_website = url_cleaner_validater(website)
            
            
            if f"www.{cleaned_website}" in [i[0] for i in self.blocked_websites] or not len(cleaned_website) or cleaned_website == "\n":
                continue            
            
            with open(self.path_website, "a") as file:
                file.write(f"www.{cleaned_website} {self.redirection} {date}\n")

            with open(self.path_hosts,"a") as hosts:
                hosts.write(f"{self.redirection} {cleaned_website}\n")
                hosts.write(f"{self.redirection} www.{cleaned_website}\n")

            self.blocked_websites.append([f"www.{cleaned_website}",self.redirection])
            return_list.append((f"www.{cleaned_website}",self.redirection,date))
        
        return return_list


    def unblock_website(self,website:str,index=int) -> None:
        """Removes website from both the Hosts file and the txt file"""

        website = url_cleaner_validater(website)
        self.blocked_websites.pop(index)
        
        #First opens the txt file, saves the lines and rewrites them in the file without the websites you want to remove
        with open(self.path_website,'r') as file:
            file_lines = file.readlines()

        with open(self.path_website,'w') as file_writerover:
            for line in file_lines:
                if website not in line:
                    file_writerover.write(line)
        
        #First opens the Hosts file, saves the lines and rewrites them in the file without the websites you want to remove
        with open(self.path_hosts,"r") as file_content:
            hosts_full_content = file_content.readlines()

        with open(self.path_hosts,"w") as hosts:
            for line in hosts_full_content:
                if line[0] == "#" or line == "\n":
                    hosts.write(line)

                #only checks second row since the redirection may be equal to the url given
                elif website not in line.split()[1]:                    
                    hosts.write(line)

    def resetter(self):
        """resetting both the hosts file and the txt file"""
        # Since there is default text in the Hosts file, we keep those in when clearing all the rest out
        with open(self.path_hosts,"r") as file_content:
             hosts_full_content = file_content.readlines()
        with open(self.path_hosts,"w") as hosts:
            for line in hosts_full_content:
                if line[0] == "#" or line == "\n":
                    hosts.write(line)

        #just fully empties the file
        with open(self.path_website,'w') as file_writerover:
            pass

        #empties the list
        self.blocked_websites = []
        
        print(f"Reset list at {datetime.datetime.now()}")


def url_cleaner_validater(url:str) -> str:
    """Returns the url without the www or https://"""
    url = url.lower().strip()
    url = "".join(url.split())

    if url.startswith("www."):
        url = re.sub("www.","",url)
    
    elif url.startswith("https://www.") or url.startswith("https://"):
        url = re.sub("https://www.","",url)
        url = re.sub("https://","",url)

    return url

class BlockedList():
    PATH_PRESET_LIST = r".\save_files\presets_blocked_lists.txt"
    
    def __init__(self):
        
        if not os.path.exists(self.PATH_PRESET_LIST):
            with open(self.PATH_PRESET_LIST,'w') as file:
                print(f"Created new file: {datetime.datetime.now()}")

        self.saved_preset_name_list = self.saved_names_retriever()
        self.name = None

    
    def get_presets_list(self) -> list:
        """Loads in the website list based on the name attribute of the class. To change the name use the name_saver(name) method"""
        with open(self.PATH_PRESET_LIST,'r') as file:
            for line in file.readlines():
                line = json.loads(line.strip())
                if line["name"] == self.name:
                    return line["websites"]
   
    def save_new_preset(self,preset_list:list) -> None:
        """Saves a new preset inside a txt file in a json format"""
        with open(self.PATH_PRESET_LIST,'a') as file:
            
            new_lst = []
            presets_dict = {"name":self.name,
                            "websites":None}
            
            for i in preset_list:
                if len(i):
                    new_lst.append(f"www.{url_cleaner_validater(i)}\n")
            
            presets_dict["websites"] = new_lst
            file.write(f"{json.dumps(presets_dict)}\n")

    def name_saver(self,name):
        """Setst then name attribute to the value inserted"""
        self.name = name

    def saved_names_retriever(self) -> list:
        """Retrieves all the already saved names"""
        presets = []
        with open(self.PATH_PRESET_LIST,"r") as file:
            for line in file.readlines():
                if line := line.strip():
                    preset_dict = json.loads(line)
                    presets.append(preset_dict["name"])
        return presets
    
    def check_availability_name(self,name):
        """Checks if a preset name is already in use"""
        if len(name):
            return any([name == i for i in self.saved_preset_name_list])
             
    def delete(self,name_del):
        """Deletes a preset inside the txt"""
        new_file_list = []

        with open(self.PATH_PRESET_LIST,'r') as file:
            for line in file.readlines():
                preset_dict = json.loads(line.strip())
                if preset_dict["name"] != name_del:
                    new_file_list.append(line)

        with open(self.PATH_PRESET_LIST,'w') as file:
            file.writelines(new_file_list)


if __name__ == "__main__":   
    print("This is the blocker.py file")

