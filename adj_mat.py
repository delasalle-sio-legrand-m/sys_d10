#coding: utf-8
elems=["eau", "air","terre","feu","glace","metal","magma","vapeur","bois","foudre"]

def makes(skill):
    return "@{{elem_{}}}".format(skill)

def makeb(skill):
    return "@{{elem_{}_buff}}".format(skill)

def maket(skill):
    return "@{{elem_{}_tot}}".format(skill)

mat_adj=[
    [2, 0, 0, 0, 1, 0, 0, 1, 1, 0],
    [0, 2, 0, 0, 1, 1, 0, 0, 0, 1],
    [0, 0, 2, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 2, 0, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 3, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 3, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 3, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 3]
]

contexts=[
    "Influence l'aptitude à prodiguer des soins et les dégats des attaques élémentaires d'eau",
    "Influence l'aptitude à générer des boucliers et les dégats des attaques élémentaires de vent",
    "Influence l'aptitude à infliger des altération d'état physiques (renversement etc...) et les dégats des attaques élémentaires de terre",
    "Influence l'aptitude à infliger des dégats et les dégats des attaques élémentaires de feu",
    "Influence l'aptitude à infliger des altération d'état magiques et les dégats des attaques élémentaires de glace",
    "Influence l'aptitude à changer les caractéristiques physiques, négativement et positivement et les dégats non élémentaires",
    "Influence l'aptitude à infliger des maux et maladies ainsi que les dégats de lave",
    "Influence l'aptitude à changer les caractéristiques magiques, négativement et positivement ainsi que les dégats toxiques",
    "Influence l'aptitude à détruire les resistances physiques, diminuer les soins et dimminuer les dégats infligés ainsi qu'augmenter les dégats de bois",
    "Influence l'aptitude à détruire les resistances magiques, les boucliers et diminuer les défences et les dégats des attaques élémentaires de foudre"
]
texts=[
    "Affinité à l'Eau (Ag)",
    "Affinité à l'Air (Int)",
    "Affinité à la Terre (For)",
    "Affinité au Feu (Psy)",
    "Affinité à la Glace (Vol)",
    "Affinité au Metal (Chn)",
    "Affinité au Magma (Chr)",
    "Affinité à la Vapeur (Per)",
    "Affinité au Bois",
    "Affinité à la Foudre"
]

addentum=[
    "Agilite",
    "Intelligence",
    "Force",
    "Psyche",
    "Volonte",
    "Chance",
    "Charisme",
    "Perception",
    "",
    ""
]


blob="""        <input class="sheet-skill_name" disabled="true" style="margin-right: 4px;" type="text" title="{contex}" name="attr_magic_elem_{elem}" value="{text}" />
        <input class="sheet-skill_name" value="1" style="margin-right: 4px;" type="number" name="attr_elem_{elem}" title="Valeur de l'affinité" />
        <input class="sheet-skill_name" value="0" style="margin-right: 4px;" type="number" name="attr_elem_{elem}_buff" title="Bonus temporaire" />
        <input class="sheet-trait" disabled="true" title="Valeur totale de l'affinité" name="attr_elem_{elem}_tot" value="{val}" />
        <br/>
"""

for i in range(10):
    mat=mat_adj[i]
    ret=''
    for j in range(10):
        if mat[j]!=0:
            e=elems[j]
            if mat[j]==1:
                ret+="{}+{}+".format(makes(e),makeb(e))
            else:
                ret+="{}*({}+{})+".format(mat[j],makes(e),makeb(e))
    ret=ret[:-1]
    if addentum[i]:
        ret+="+(@{{base-{c}}}+@{{exal-{c}}})*20".format(c=addentum[i])

    print(blob.format(contex=contexts[i], elem=elems[i],text=texts[i],val="floor({}/10)".format(ret)))
