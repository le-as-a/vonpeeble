import discord
from discord import Embed, Colour, SelectOption
from db.api.calling import get_calling
from db.api.ability import get_abilities, get_ability
from db.api.character_ability import get_entries, new_entry
from db.api.character import rank_up
from views.RankupView import RankupView

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