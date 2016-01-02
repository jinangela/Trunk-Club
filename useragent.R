# Read data from Greenplum into R:
library("RPostgreSQL", lib.loc="~/R/win-library/3.2")
drv <- dbDriver("PostgreSQL")
conn <- dbConnect(drv,user="mjin",password="Efj2xGCQ%rCksw6b",dbname="scratch",host="gpdb",port="5432")
raw <- dbReadTable(conn,c("trunkclub","original"))
dbDisconnect(conn)
setwd("/Users/mjin/Desktop/TrunkClub_Mengshan")

# I use the following two websites to help me determine which browser the user is using
# https://www.whatismybrowser.com/developers/tools/user-agent-parser/
# http://webaim.org/blog/user-agent-string-history/
useragent <- subset(raw,select=c(taskid,useragent))

######################Device and OS############################
# iPhone Users
temp1 <- grep(".*iPhone.*",raw$useragent)
temp2 <- grep(".*iPad.*",raw$useragent)
iphoneindex <- setdiff(temp1,temp2)
iphone <- raw$useragent[iphoneindex]
# Android Phone Users
temp1 <- grep(".*Android.*",raw$useragent)
temp2 <- grep(".*Android.*Tablet.*",raw$useragent)
androidindex <- setdiff(temp1,temp2)
android <- raw$useragent[androidindex] 
# Windows Phone Users
wpindex <- grep(".*Windows Phone.*",raw$useragent)
windowsphone <- raw$useragent[wpindex] 
# Blackberry Users
bbindex <- grep(".*[(]BB.*",raw$useragent)
blackberry <- raw$useragent[bbindex] 

# iPad Users
ipadindex <- grep(".*iPad.*",raw$useragent)
ipad <- raw$useragent[ipadindex]
# Android Tablet Users
atindex <- grep(".*Android.*Tablet.*",raw$useragent)
atablet <- raw$useragent[atindex]
# Windows Tablet Users
wtindex <- grep(".*Tablet PC.*",raw$useragent)
wtablet <- raw$useragent[wtindex]

# iPod Users
ipodindex <- grep(".*iPod.*",raw$useragent)
ipod <- raw$useragent[ipodindex]

# Mac OS X Users
macindex <- grep(".*Macintosh.*Mac OS X.*",raw$useragent)
mac <- raw$useragent[macindex]
# Windows OS Users
temp1 <- grep(".*Windows Phone.*",raw$useragent)
temp2 <- grep(".*compatible.*MSIE.*Windows NT.*",raw$useragent)
notinclude <- union(temp1,temp2)
include <- grep(".*Windows.*",raw$useragent)
windex <- setdiff(include,notinclude)
windows <- raw$useragent[windex]
#### test ####
include <- grep(".*Windows NT.*",raw$useragent)
index <- setdiff(include,notinclude)
test <- raw$useragent[index] # the result is the same
# Windows Server Users
temp1 <- grep(".*compatible.*MSIE.*Windows NT.*",raw$useragent)
temp2 <- grep(".*Tablet PC.*",raw$useragent)
wsindex <- setdiff(temp1,temp2)
wserver <- raw$useragent[wsindex]
# X Window System Users
# xindex <- grep(".*[(]X11.*",raw$useragent)
# xwindow <- raw$useragent[xindex]
crindex <- grep(".*[(]X11; CrOS.*",raw$useragent)
cros <- raw$useragent[crindex]
linuxindex <- grep(".*[(]X11; Linux.*",raw$useragent)
linux <- raw$useragent[linuxindex]
ubuntuindex <- grep(".*[(]X11; Ubuntu.*",raw$useragent)
ubuntu <- raw$useragent[ubuntuindex]
# temp <- setdiff(xindex,union(union(crindex,linuxindex),ubuntuindex))
# raw$useragent[temp]

#### test ####
cover <- union(iphoneindex,androidindex)
cover <- union(cover,wpindex)
cover <- union(cover,bbindex)
cover <- union(cover,ipodindex)
cover <- union(cover,ipadindex)
cover <- union(cover,atindex)
cover <- union(cover,wtindex)
cover <- union(cover,macindex)
cover <- union(cover,windex)
cover <- union(cover,wsindex)
cover <- union(cover,crindex)
cover <- union(cover,linuxindex)
cover <- union(cover,ubuntuindex)
total <- which(raw$useragent!="")
left1 <- setdiff(total,cover)

#########################browser and app##########################
# IE Users
ieindex <- union(grep(".*like Gecko$",raw$useragent),grep(".*Trident.*",raw$useragent))
ie <- raw$useragent[ieindex]
# Firefox Users
firefoxindex <- grep(".*Firefox.*",raw$useragent)
firefox <- raw$useragent[firefoxindex]
# PC Chrome Users
include <- grep(".*Chrome.*",raw$useragent)
notinclude <- union(grep(".*Chrome.*Mobile Safari.*",raw$useragent),grep(".*Mobile Safari.*Chrome.*",raw$useragent))
chromeindex <- setdiff(include,notinclude)
chrome <- raw$useragent[chromeindex]
#### test ####
test <- raw$useragent[grep(".*Chrome.*Safari.*",raw$useragent)]
index <- setdiff(grep(".*Chrome.*",raw$useragent),grep(".*Chrome.*Safari.*",raw$useragent))
test <- raw$useragent[index]
# Windows Safari Users
winsafariindex <- grep(".*Windows.*Safari.*",raw$useragent)
winsafari <- raw$useragent[winsafariindex]
# iOS Safari Users
temp1 <- grep(".*Android.*",raw$useragent)
temp2 <- grep(".*Chrome.*",raw$useragent)
temp3 <- grep(".*[(]BB.*",raw$useragent)
notinclude <- union(union(temp1,temp2),temp3)
notinclude <- union(notinclude,winsafariindex)
include <- grep(".*Safari.*",raw$useragent)
safariindex <- setdiff(include,notinclude)
safari <- raw$useragent[safariindex]

# iOS Trunk Club app Users
temp1 <- union(grep(".*app.*iOS.*",raw$useragent),grep(".*TrunkClub.*iOS.*",raw$useragent))
iosappindex <- union(temp1,grep("^com\\.trunkclub\\.member.*iOS.*",raw$useragent))
iosapp <- raw$useragent[iosappindex]
# same as app <- raw$useragent[grep(".*app.*",raw$useragent)]
# Android Trunk Club app Users
andappindex <- grep(".*TrunkClubMember.*Android.*",raw$useragent)
androidapp <- raw$useragent[andappindex]
# same as androidapp <- raw$useragent[grep(".*TrunkClubMember.*",raw$useragent)]

# Mobile Chrome Users
mcindex <- union(grep(".*Chrome.*Mobile Safari.*",raw$useragent),grep(".*Mobile Safari.*Chrome.*",raw$useragent))
mchrome <- raw$useragent[mcindex]
# Unknown iOS Mobile Browser Users
umbindex <- union(grep(".*iPhone.*Mobile/.*",raw$useragent),grep(".*iPad.*Mobile/.*",raw$useragent))
umbrowser <- raw$useragent[umbindex]
# Android Browser Users
abindex <- setdiff(grep(".*Android.*AppleWebKit.*",raw$useragent),mcindex)
abrowser <- raw$useragent[abindex]
# Blackberry Browser Users
bbbrowserindex <- grep(".*[(]BB.*Mobile.*",raw$useragent)
bbbrowser <- raw$useragent[bbbrowserindex]

# Facebook Users
include <- grep(".*FB.*",raw$useragent)
fbindex <- setdiff(include,mcindex)
facebook <- raw$useragent[fbindex]
# Twitter Users
twindex <- grep(".*Twitter.*",raw$useragent)
twitter <- raw$useragent[twindex]
# Instagram Users
insindex <- grep(".*Instagram.*",raw$useragent)
instagram <- raw$useragent[insindex]

#### test ####
cover <- union(ieindex,firefoxindex)
cover <- union(cover,chromeindex)
cover <- union(cover,winsafariindex)
cover <- union(cover,safariindex)
cover <- union(cover,iosappindex)
cover <- union(cover,andappindex)
cover <- union(cover,mcindex)
cover <- union(cover,fbindex)
cover <- union(cover,twindex)
cover <- union(cover,umbindex)
cover <- union(cover,insindex)
cover <- union(cover,abindex)
cover <- union(cover,bbbrowserindex)
total <- which(raw$useragent!="")
left2 <- setdiff(total,cover)

#### Create Categorical Variables ####
device <- vector(mode = "character", length = nrow(raw))
OS <- vector(mode = "character", length = nrow(raw))
apptype <- vector(mode = "character", length = nrow(raw))
appname <- vector(mode = "character", length = nrow(raw))

device[iphoneindex] = "iPhone"
device[androidindex] = "Android Phone"
device[wpindex] = "Windows Phone"
device[bbindex] = "Blackberry"
device[ipadindex] = "iPad"
device[atindex] = "Android Tablet"
device[wtindex] = "Windows Tablet"
device[ipodindex] = "iPod"
device[macindex] = "MacBook"
device[windex] = "PC"
device[wsindex] = "Windows Server"
device[crindex] = "ChromeBook"
device[linuxindex] = "Linux"
device[ubuntuindex] = "Ubuntu"
device[left1] = "Other"

appname[ieindex] = "IE"
appname[firefoxindex] = "Firefox"
appname[chromeindex] = "Desktop Chrome"
appname[winsafariindex] = "Windows Safari"
appname[safariindex] = "iOS Safari"
appname[iosappindex] = "iOS Trunk Club app"
appname[andappindex] = "Android Trunk Club app"
appname[mcindex] = "Mobile Chrome"
appname[umbindex] = "Unknown iOS Mobile Browser"
appname[abindex] = "Android Browser"
appname[bbbrowserindex] = "Blackberry Browser"
appname[fbindex] = "Facebook"
appname[twindex] = "Twitter"
appname[insindex] = "Instagram"
appname[left2] = "Other"

# The following two are generalized and hope they can help in further analysis
OS[iphoneindex] = "iOS"
OS[androidindex] = "Android"
OS[wpindex] = "Windows"
OS[bbindex] = "Blackberry"
OS[ipadindex] = "iOS"
OS[atindex] = "Android"
OS[wtindex] = "Windows"
OS[ipodindex] = "iOS"
OS[macindex] = "OS X"
OS[windex] = "Windows"
OS[wsindex] = "Windows"
OS[crindex] = "Chrome OS"
OS[linuxindex] = "Linux"
OS[ubuntuindex] = "Ubuntu"
OS[left1] = "Other"

apptype[ieindex] = "browser"
apptype[firefoxindex] = "browser"
apptype[chromeindex] = "browser"
apptype[winsafariindex] = "browser"
apptype[safariindex] = "browser"
apptype[iosappindex] = "app"
apptype[andappindex] = "app"
apptype[mcindex] = "app"
apptype[umbindex] = "app"
apptype[abindex] = "app"
apptype[bbbrowserindex] = "app"
apptype[fbindex] = "app"
apptype[twindex] = "app"
apptype[insindex] = "app"
apptype[left2] = "Other"

useragent <- cbind(useragent,device,OS,apptype,appname)