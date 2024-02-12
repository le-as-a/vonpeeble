from db.api.calling import get_calling

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


