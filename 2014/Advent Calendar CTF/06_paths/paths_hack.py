import sys

E = [[(96, 65)], [(64, 99)], [(24, 88)], [(75, 48)], [(63, 66)], [(38, 55)], [(98, 113)], [(99, 104)], [(46, 72)], [(22, 108)], [(28, 65)], [(36, 74)], [(87, 110)], [(64, 72)], [(98, 52)], [(29, 100)], [(17, 66)], [(89, 85)], [(46, 48)], [(85, 98)], [(29, 102)], [(44, 66)], [(22, 105)], [(83, 97)], [(19, 108)], [(40, 80)], [(48, 74)], [(53, 107)], [(9, 120)], [(59, 67)], [(79, 95)], [(91, 122)], [(73, 107)], [(75, 84)], [(3, 119)], [(94, 51)], [(19, 97)], [(77, 117)], [(85, 52)], [(24, 72)], [(30, 121)], [(35, 67)], [(21, 110)], [(29, 75)], [(35, 53)], [(1, 57)], [(72, 101)], [(44, 68)], [(44, 72)], [(80, 86)], [(28, 84)], [(96, 55)], [(65, 89)], [(90, 49)], [(47, 84)], [(31, 119)], [(88, 66)], [(61, 110)], [(82, 114)], [(74, 53)], [(34, 89)], [(6, 80)], [(0, 122)], [(41, 77)], [(55, 76)], [(55, 118)], [(18, 89)], [(63, 67)], [(66, 110)], [(96, 116)], [(69, 70)], [(57, 107)], [(70, 84)], [(58, 48)], [(69, 112)], [(12, 102)], [(17, 73)], [(51, 117)], [(94, 95)], [(70, 107)], [(50, 76)], [(76, 82)], [(58, 77)], [(23, 65)], [(85, 108)], [(30, 53)], [(61, 121)], [(69, 103)], [(79, 86)], [(72, 122)], [(46, 79)], [(66, 105)], [(79, 111)], [(75, 70)], [(72, 67)], [(41, 65)], [(94, 68)], [(58, 79)], [(67, 50)], []]

start = 0
goal = 99

F = [0 for x in range(100)]
for i in range(len(E)-1):
    F[E[i][0][0]]=i

print F

