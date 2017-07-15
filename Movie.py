class Movie:
        def __init__(self):
                self.title = ""
                self.link = ""
                self.link1080p = ""
                self.link720p = ""
                self.link3D = ""

        def __str__(self):
                return "Title: " + self.title + "\nLink: " + self.link + "\nPic: " + self.link720p + "\n" 

        def __repr__(self):
                return self.__str__()