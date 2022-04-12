file_txt = "entradaProj2TAG.txt"


"""
    * Criação de dois dicionários: 
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

"""
    * Aqui estou retornando um índice no qual um estudante será inserido, conforme sua nota e sua preferência
"""
def Index_Por_Nota_e_Preferencia(students, list, s, p):
    nota_estudante = students[s]["nota"]
    preferencias_estudante = students[s]["preferencias"].index(p)
    
    for i in range(len(list)-1, -1, -1):
        nota_ = students[list[i]]["nota"]
        preferencia = students[list[i]]["preferencias"].index(p)
        
        if nota_estudante == nota_:
            if preferencias_estudante >= preferencia:
                return i + 1
        elif nota_estudante < nota_:
            return i + 1
    
    return i

"""
    * Aqui estou armazenando em uma lista, as preferências dos projetos por estudantes
"""
def Preferencias_por_projeto(projetos, estudantes):
    preferencias_projetos = dict()
    
    for p in projetos.keys():
        preferencias_projetos[p] = projetos[p].copy()
        estudante_por_projeto = []
        
        for s in estudantes.keys():
            if p in estudantes[s]["preferencias"]:
                if len(estudante_por_projeto) == 0:
                    estudante_por_projeto.append(s)
                else:
                    i = Index_Por_Nota_e_Preferencia(estudantes, estudante_por_projeto, s, p)
                    estudante_por_projeto.insert(i, s)
            
        preferencias_projetos[p]["preferencias"] = estudante_por_projeto
    
    return preferencias_projetos

"""
    * Executando algoritmo GALE-SHAPLEY. Algoritmo que dá prioridade aos projetos nos quais preferências por nota de 
      aluno já está estabelecida pelo arquivo de entrada.
    * Os projetos optam por preferir alunos com maiores notas e que preferem o mesmo projeto
"""
def Gale_Shapley(projects, students):
    matchings = []
    proj = []
    estud = []
    
    propostas_proj = {p: [] for p in projects.keys()} # estudantes já avaliados em cada projeto
    
    print_10 = 0 

    set_proj = [p for p in projects.keys() if (p not in proj) and len(propostas_proj[p]) != len(projects[p]["preferencias"])]
    
    while len(set_proj) != 0:
        print_etapas = 0 # Para  impressão de etapas
        p = set_proj[0]    
        s = [s for s in projects[p]["preferencias"] if s not in propostas_proj[p]][0]

        limite = projects[p]['vagas']
        nota_minima_p = projects[p]['nota_minima']

        if students[s]['nota'] >= nota_minima_p:
            print_etapas = 1
            if s not in estud:
                matchings.append([p, s])
                estud.append(s)
            else:
                estud_act_proj = [mat for mat in matchings if mat[1] == s][0][0]

                if students[s]["preferencias"].index(p) < students[s]["preferencias"].index(estud_act_proj):
                    print_etapas = 2
                    if estud_act_proj in proj:
                        proj.pop(proj.index(estud_act_proj))

                    matchings.pop(matchings.index([estud_act_proj, s]))
                    matchings.append([p, s])

                    estud.append(s)

            act_n_memb = len([mat for mat in matchings if mat[0] == p])

            # Retirar projeto em caso de lotação
            if act_n_memb == limite:
                proj.append(p)

        propostas_proj[p].append(s)
        set_proj = [p for p in projects.keys() if (p not in proj) and len(propostas_proj[p]) != len(projects[p]["preferencias"])]
        
        if print_10 < 10:
            if print_etapas != 2:
                estud_act_proj = None
            
            full_p = act_n_memb == limite
            all_checked_p = len(propostas_proj[p]) == len(projects[p]["preferencias"])
            print_text(print_10, print_etapas, p, s, full_p, all_checked_p, estud_act_proj)
            
            print_10 = print_10 + 1
    
    return matchings

"""
    Organizando os emparelhamentos realizados na lista para um dicionário que contém os projetos como chave
"""
def Organizar(mat):
    matchings = dict()
    
    k_list = set([int(m[0].replace('P', '')) for m in mat])
    k_list = sorted(list(k_list))
    k_list = ['P' + str(k) for k in k_list]
    
    for k in k_list: 
        estudantes = sorted([int(m[1].replace('A', '')) for m in mat if m[0] == k])
        estudantes = ['A' + str(s) for s in estudantes]
        matchings[k] = estudantes
    
    return matchings

"""
    * Removendo projetos nos quais vagas não foram totalmente preenchidas
    * Organizando projetos descartados por falta de inscrições
"""
def Remover_projetos_nao_preenchidos(projetos_match, projects):
    projetos_out = dict()
    projetos_out_list = []
    
    projetos_out_list = [k for k in projetos_match.keys() if len(projetos_match[k]) < projects[k]["vagas"]]
    projetos_out_list += [k for k in projects.keys() if k not in projetos_match.keys()]
            
    for r in projetos_out_list:
        if r in projetos_match.keys():
            projetos_out[r] = projetos_match[r]
            projetos_match.pop(r)
        else:
            projetos_out[r] = []
        
    return projetos_match, projetos_out


"""
    Prints para melhor compreensão
"""
def print_text(i, sub, p, s, full_p=False, all_checked_p=False, p_ant_of_s=None):
    if i == 0:
        print("\n")
        print("10 primeiras iterações a seguir")
        print("\n")
    
    if sub == 0:
        txt_loop = "{0}: {1}     X     {2} (par impossível)".format(i+1, p, s)
    elif sub == 1:
        txt_loop = "{0}: {1} --> {2} (par formado)".format(i+1, p, s)
    else:
        txt_loop = "{0}: {1} --/--> {2} (par desfeito)\n     {3} --> {2} (par formado)".format(i+1, p_ant_of_s, s, p)

    if full_p:
        txt_loop += "\n *{0} cheio\n".format(p)
    if all_checked_p:
        txt_loop += "\n *{0} checou todos inscritos\n".format(p)

    print(txt_loop)

def print_matchings(mat, rem_mat):
    print("\n\n")
    print("Emparelhamento estável máximo obtido:")
    print("    *     Quantidade de projetos com estudantes alocados (vagas preenchiads): {0}".format(len(mat)))
    print("    *     Quantidade de projeto descartados: {0}".format(len(rem_mat)))
    print("\n")

def print_projetos_matching(mat, projects, full):
    if full:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Projetoscom todas vagas preenchidas:<\n")
    else:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Projetos com vagas sobrando (descartados):<\n")
    
    for p in mat.keys():
        ef_insc = len(mat[p])
        av_insc = projects[p]["vagas"]

        txt_insc = "inscrições"
        txt_vag = "vagas"
        if ef_insc == 1:
            txt_insc = "inscrição"
        if av_insc == 1:
            txt_vag = "vaga"

        txt_full = "{0}: ---> {1}\n    ({2} {3} X {4} {5})\n".format(p, str(mat[p]).replace("'", ""), ef_insc, txt_insc, av_insc, txt_vag)

        print(txt_full)


projects, students = Projetos_e_Estudantes(file_txt)
projects = Preferencias_por_projeto(projects, students)

mat = Gale_Shapley(projects, students)
mat = Organizar(mat)
mat, rem_mat = Remover_projetos_nao_preenchidos(mat, projects)

# Print das informaçõs em relação ao emparelhamento encontrado
print_matchings(mat, rem_mat)
print_projetos_matching(mat, projects, full=True)
print_projetos_matching(rem_mat, projects, full=False)