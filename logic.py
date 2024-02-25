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
