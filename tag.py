file_txt = "entradaProj2TAG.txt"


"""
Criação de dois dicionários: 
    projects: todos os projetos com suas respectivas vagas e nota mínima para aceitação
    students: todos os estudantes com suas respctivas preferências e nota atriuida
"""
def Projetos_e_Estudantes(file):
    with open(file) as f:
        lines = f.readlines()
    f.close()

    projetos = []
    estudantes = []

    for line in lines:
        if line[0:2] == '(P':
            projetos.append(line)
        elif line[0:2] == '(A':
            estudantes.append(line)

    for index in range(len(projetos)):
        projetos[index] = projetos[index].replace('\n', '').replace('(', '').replace(')', '').replace(' ', '').split(',')

    projects = {p[0]: {"vagas": int(p[1]), "nota_minima": int(p[2])} for p in projetos}
    students = []

    for estudante in estudantes:
        estudante = estudante.replace("\n", "").replace(" ", "")

        id = estudante.split(":")[0]
        estudante = estudante.split(":")[1]
        id = id.replace("(", "").replace(")", "")
        nota = estudante.split(")(")[1]
        estudante = estudante.split(")(")[0]
        nota = nota.replace(")", "")
        preferencias = estudante.replace("(", "").replace(")", "").split(",")
        students.append([id, preferencias, nota])
    
    students = {s[0]: {"preferencias": s[1], "nota": int(s[2])} for s in students}

    return projects, students





# Projetos_e_Estudantes(file_txt)