In a typical enterprise, a separate group of people, Installers, are responsible for install new devices. May it be a new installation (e.g. new stores), a replacement installation (e.g. replacing Cisco APs with Mist APs), or addition (e.g. adding new APs for better coverage). Instead of granting them Admin/Write privilege, it's more desirable to grant them minimum privileges to do the initial provisioning so they cannot read sensible information (e.g. PSK of a WLAN), or change configs of running APs.
At a high level, Installer APs try to achieve the following:
1. identifying a device by MAC (that\u2019\
s what they see)
2. they can only touch configurations of the devices they\u2019\
re installing
3. allow the following configurations: 
  * name * site assignment 
  * device profile assignment 
  * map and location (x/y) assignment 
  * claim (if not already in the inventory) 
  * replace existing device with the device being installed

**Grace Period**

Grace period provides a dynamic way to limit what devices / sites installer can work on. Generally installers work on recent deployments - bringing up new sites, add newly claimed devices to new / existing sites. They make mistakes, too, and may need to further tweak some of the parameters. Default grace period is 7 days and can be set from 1 day to 365 days.