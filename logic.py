import discord
from db.api.calling import get_calling
from random import randint

def good_stat(trait, might, deftness, grit, insight, aura):
    match trait:
        case 'Might':
            might += 1
        case 'Deftness':
            deftness += 1
        case 'Grit':
            grit += 1
        case 'Insight':
            insight += 1
        case 'Aura':
            aura += 1
    return (might, deftness, grit, insight, aura)

def bad_stat(trait, might, deftness, grit, insight, aura):
    match trait:
        case 'Might':
            might -= 1
        case 'Deftness':
            deftness -= 1
        case 'Grit':
            grit -= 1
        case 'Insight':
            insight -= 1
        case 'Aura':
            aura -= 1
    return (might, deftness, grit, insight, aura)

def generate_stats(calling, rank, species, good1, good2, bad):
    (might, deftness, grit, insight, aura) = get_calling(calling, rank)
    match species:
        case species if species in ['Chib', 'Goblin']:
            might -= 1
            deftness += 1
        case species if species in ['Gruun', 'Promethean']:
            might += 1
    (might, deftness, grit, insight, aura) = good_stat(good1, might, deftness, grit, insight, aura)
    (might, deftness, grit, insight, aura) = good_stat(good2, might, deftness, grit, insight, aura)
    (might, deftness, grit, insight, aura) = bad_stat(bad, might, deftness, grit, insight, aura)
    return (might, deftness, grit, insight, aura)

def customized(calling):
    url = ''
    color = ''
    match calling:
        case 'Factotum':
            url = "https://i.imgur.com/mifSzqX.png"
            color = '693d17'
        case 'Sneak':
            url = "https://i.imgur.com/Po1gbO5.png"
            color = '757575'
        case 'Champion':
            url = "https://i.imgur.com/LVik76H.png"
            color = 'FFFFFF'
        case 'Raider':
            url = "https://i.imgur.com/4zyyl2H.png"
            color = '5b9623'
        case 'Battle Mage':
            url = "https://i.imgur.com/UIlytfb.png"
            color = 'e4bee6'
        case 'Murder Noble':
            url = "https://i.imgur.com/bngxKbu.png"
            color = 'de0977'
        case 'Sage':
            url = "https://i.imgur.com/e5uB97H.png"
            color = '57d7e6'
        case 'Heretic':
            url = "https://i.imgur.com/N1Zh5KB.png"
            color = '5d358f'
    return (url, color)

def qColor(quirk_type):
    match quirk_type:
        case 'Spirit':
            color = '95f5ed'
        case 'Physiology':
            color = 'f0975b'
        case 'Fate':
            color = '8367b8'
        case 'Eldritch':
            color = 'e3d21b'
        case 'Robotic':
            color = 'd4d4d4'
    
    return color

def qImg(quirk_name):
    images = {
        "Adorable": "https://i.imgur.com/R2iNILK.png",
        "Always Prepared": "https://i.imgur.com/ptKPu4A.png",
        "Angelic Countenance": "https://i.imgur.com/iI4EHbC.png",
        "Battle Scanner": "https://i.imgur.com/d3079fe.png",
        "Beast Tongue": "https://i.imgur.com/kmiIPJz.png",
        "Big Eater": "https://i.imgur.com/Zc8Bg3J.png",
        "Bioskin": "https://i.imgur.com/BBBlFez.png",
        "Boring": "https://i.imgur.com/8jk25J1.png",
        "Buster Arm": "https://i.imgur.com/PwcHvO7.png",
        "Clear Intent": "https://i.imgur.com/yRbP4zq.png",
        "Crowned": "https://i.imgur.com/yb42p6B.png",
        "Curious": "https://i.imgur.com/Y536ILH.png",
        "Dark Demeanor": "https://i.imgur.com/1uDrkSz.png",
        "Destined": "https://i.imgur.com/qfB0yUK.png",
        "Dread Orator": "https://i.imgur.com/IiS8mGQ.png",
        "Dreamer": "https://i.imgur.com/k7pwItu.png",
        "Fairy Cap": "https://i.imgur.com/0tAacfL.png",
        "Ferrous": "https://i.imgur.com/cehVW2M.png",
        "Figment Follower": "https://i.imgur.com/H7uqXCa.png",
        "Girthsome": "https://i.imgur.com/RlKfKo5.png",
        "Grasping Tresses": "https://i.imgur.com/Jrf8Ih0.png",
        "Guardian": "https://i.imgur.com/CZC789e.png",
        "Industrial Frame": "https://i.imgur.com/XrJwT3L.png",
        "Infested": "https://i.imgur.com/c1wcTlg.png",
        "Jumpy": "https://i.imgur.com/yjhFxQC.png",
        "Lyrical": "https://i.imgur.com/6bWtcRk.png",
        "Mage Breaker": "https://i.imgur.com/0vKJWqw.png",
        "Mascot Chassis": "https://i.imgur.com/aWikBoe.png",
        "Masked": "https://i.imgur.com/YJhoQpX.png",
        "Miser": "https://i.imgur.com/5gZNFo4.png",
        "Nanotech Maintenance": "https://i.imgur.com/U5q4RIB.png",
        "Nearsighted": "https://i.imgur.com/1xYrQUo.png",
        "Nox-Vision": "https://i.imgur.com/HAkSN9G.png",
        "Past Injury": "https://i.imgur.com/vBvc2FM.png",
        "Peculiar Taste": "https://i.imgur.com/Ts6Wgbu.png",
        "Pedantic": "https://i.imgur.com/IeqEu2u.png",
        "Sneezles": "https://i.imgur.com/YySHNOe.png",
        "Soul Link": "https://i.imgur.com/yXFVmHL.png",
        "Sproing Sprockets": "https://i.imgur.com/MKXjWBw.png",
        "Stylish": "https://i.imgur.com/vP0cpSj.png",
        "Survivor": "https://i.imgur.com/jtZnKHR.png",
        "Translator Module": "https://i.imgur.com/629d711.png",
        "Unhinged": "https://i.imgur.com/Omb1IqU.png",
        "Utility Servo": "https://i.imgur.com/mPDRcGI.png",
        "Waifish": "https://i.imgur.com/RRJfgRl.png",
        "Weary": "https://i.imgur.com/TEGxVH4.png",
        "Winged": "https://i.imgur.com/Uee4nk5.png",
        "Young": "https://i.imgur.com/YL0gn3Y.png"
    }
    return images[quirk_name]

def apt_check(aptitude):
    color = ''
    match aptitude:
        case 'Might':
            color = 'fca103'
        case 'Deftness':
            color = '69b802'
        case 'Grit':
            color = 'b80245'
        case 'Insight':
            color = '00e7eb'
        case 'Aura':
            color = 'ba45d1'
    return color

def injury_table(severity, roll):
    injury = ""
    first = severity == 1
    second = severity == 2
    third = severity == 3
    special_roll = ""
    img = ""
    match roll:
        case roll if (first and roll in range(1, 5)) or (second and roll in range(1, 3)) or (third and roll in [1,2]):
            injury = f"## Rolled a {roll} and became Shocked/Stalled\nA solid blow has stunned you.\n---\nMiss your next Combat Turn."
            img = "https://i.imgur.com/dpVr89S.png"
        case roll if (first and roll in range(6,10)) or (second and roll in range(4, 6)) or (third and roll in [3,4]):
            injury = f"## Rolled a {roll} and got an Armor Crash\nYour armor absorbs a dangerous blow.\n---\nYour armor's Defense Bonus is reduced by 2. This penalty lasts until your armor is repaired. When your Armor Bonus is reduced to 0, your armor is destroyed. If you are not wearing armor, count this Injury as Wounded."
            img = "https://i.imgur.com/y5Kpzzb.png"
        case roll if (first and roll in range(11, 14)) or (second and roll in range(7,9)) or (third and roll in [5,6]):
            injury = f"## Rolled a {roll} and became Wounded\nYou've taken a non-fatal but significant wound.\n---\nYour maximum Hearts Total is reduced by 1 until you receive Treatment for this Injury. If this Injury reduces your Hearts Total to 0, count this Injury as Quiet Death."
            img = "https://i.imgur.com/3Whqn8c.png"
        case roll if (first and roll in [15,16]) or (second and roll in [10,11]) or (third and roll in [7,8]):
            injury = f"## Rolled a {roll} and got a Broken Arm\nA blow to your arm has left it useless.\n---\nRoll to see which arm is broken. (1-10 right arm, 11-20 left arm). Your Might Aptitude is halved when making Checks or Contests requiring the use of your arms until you receive Treatment for this Injury. If this Injury occurs on the same limb a second time, count this Injury as Severed."
            special_roll = "Broken arm"
            img = "https://i.imgur.com/TPbzaza.png"
        case roll if (first and roll in [17,18]) or (second and roll in [12,13]) or (third and roll in [9,10]):
            injury = f"## Rolled a {roll} and got a Broken Leg\nA strike to your leg forces you to hobble or crawl.\n---\nRoll to see which leg is broken (1-10 right leg, 11-20 left leg). Your Speed Rating is reduced by a single step. You suffer a Snag on all Might and Deftness Aptitude Checks and Contests requiring the use of your legs until you receive Treatment for this Injury. If this Injury occurs on the same limb a second time, count this Injury as Severed."
            special_roll = "Broken leg"
            img = "https://i.imgur.com/WQp2r15.png"
        case roll if (first and roll in [19,20]) or (second and roll in [14,15]) or (third and roll in [11,12]):
            injury = f"## Rolled a {roll} and got knocked Out Cold\nYou are knocked senseless and out for the rest of the fight.\n---\nYou fall to the ground and can no longer participate in the Fight. You will regain consciousness once the Fight is over and suffer no lasting damage. An enemy can slay you immediately if they are unhindered and use their Turn to do so. If you receive First Aid you will be revived but cannot use any Combat Actions for the remainder of the Fight."
            img = "https://i.imgur.com/dCEihfQ.png"
        case roll if (second and roll in [16,17]) or (third and roll in [13,14]):
            injury = f"## Rolled a {roll} and are Near Death\nYou're dying, and need urgent attention.\n---\nYou'll die within 2 Turns if help doesn't arrive. First Aid reduces this Injury to Wounded."
            img = "https://i.imgur.com/AOoj7Jb.png"
        case roll if (second and roll == 18) or (third and roll in [15,16]):
            injury = f"## Rolled a {roll} and got Severed\nA limb is sliced off, crushed, or otherwise detached.\n---\nRoll to see which limb is severed (1-5 right arm, 6-10 left arm, 11-15 right leg, 16-20 left leg). You'll need Magical Treatment or Prosthetic Replacement to regain the limb's function. Until replaced, consider a severed arm as the Broken Arm Injury, and a severed leg as the Broken Leg Injury, except you obviously cannot use your severed limb at all. Re-roll if the limb has already been severed and not been replaced. If you have no limbs left, you've been decapitated and are dead."
            special_roll = "Severed"
            img = "https://i.imgur.com/FmdvI1F.png"
        case roll if (second and roll == 19) or (third and roll == 17):
            injury = f"## Rolled a {roll} and are Mutilated\nYou're dying and need urgent attention. Even if saved, the injury is so terrible it will leave you debilitated.\n---\nYou'll die within 2 Turns if help doesn't arrive. First Aid will prevent your death but... you suffer a -1 penalty to an Aptitude of your choice which is related to the would. For example, -1 Insight for a head blow.\n**Bio-Mechanoid?** You lose your Robotic Quirk. The second time you receive this Injury, suffer the Aptitude penalty above. Magical/Advanced Treatment is required to remove the lasting effect of the Injury."
            img = "https://i.imgur.com/ZNo5557.png"
        case roll if (second and roll == 20) or (third and roll == 18):
            injury = f"## Rolled a {roll} and suffer a Mortal Wound\nYou've been impaled, beaten, or lacerated in such a way that death is imminent.\n---\nYou have received a fatal blow and will die, no Treatment can save you. You may take on last Action on your next Turn before expiring. Make it count! Your body is recoverable, so perhaps there is a chance at some unnatural ressurection...\n**Bio-Mechanoid?** You lie not dead, but offline. You have one chance at being rebooted but the Advanced Treatment will suffer a Snag. Failing this, maybe your core could be transferred to an alternative shell."
            img = "https://i.imgur.com/Y2T49ql.png"
        case roll if third and roll == 19:
            injury = f"## Rolled a {roll} and get a Quiet Death\nYou are killed instantly, without theatrics.\n---\nYou are dead. Your body is recoverable, so perhaps there is a chance at some unnatural resurrection..."
            img = "https://i.imgur.com/9jo0k7j.png"
        case roll if third and roll == 20:
            injury = f"## Rolled a {roll} and became a Messy Affair\nYou've been splattered, disintegrated, or otherwise scrubbed from existence.\n---\nYou are dead. The fatal blow leaves little that is recognisable.\n**Bio-Mechanoid?** Make a Grit Check. Failure results in an explosion doing 2 Hearts of Damage to anyone in the same Area as you. If you succeed, you fall to pieces on the spot."
            img = "https://i.imgur.com/5LkfZEU.png"
        
    return (injury, special_roll, img)
        
def specRoll(roll_type):
    res = ""
    roll = randint(1, 20)
    coin_flip = roll in range(1,10)
    match roll_type:
        case 'Broken arm':
            if coin_flip:
                res = f"\n---\n### You rolled a {roll} and break your right arm."
            else:
                res = f"\n---\n### You rolled a {roll} and break your left arm."
        case 'Broken leg':
            if coin_flip:
                res = f"\n---\n### You rolled a {roll} and break your right leg."
            else:
                res = f"\n---\n### You rolled a {roll} and break your left leg."
        case 'Severed':
            if roll in range(1, 5):
                res = f"\n---\n### You rolled a {roll} and lose your right arm."
            elif roll in range (6,10):
                res = f"\n---\n### You rolled a {roll} and lose your left arm."
            elif roll in range(11,15):
                res = f"\n---\n### You rolled a {roll} and lose your right leg."
            else:
                res = f"\n---\nYou rolled a {roll} and lose your left leg."
    
    return res