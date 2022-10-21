lista_de_slices={
    "slice1":{
    "imagem_att": "ID_000f0bd99.png",
    "brain":"ID_00fdec745.png",
    "subdural":"ID_000f0bd99.png",
    "bone":"ID_00ed02fcc.png",
    "heatmap":"ID_00fdec745.png",
    "probabilidade":1
      },

    "slice2":{
    "imagem_att": "ID_000f0bd99.png",
    "brain":"ID_00fdec745.png",
    "subdural":"ID_000f0bd99.png",
    "bone":"ID_00ed02fcc.png",
    "heatmap":"ID_00fdec745.png",
    "probabilidade":2
      },
      "slice3":{"probabilidade":3},
      "slice4":{"probabilidade":4},
      "slice5":{"probabilidade":5},
      "slice6":{"probabilidade":6},
      "slice7":{"probabilidade":7}
}

lista={ "imagem_att": "ID_000f0bd99.png",
    "brain":"ID_00fdec745.png",
    "subdural":"ID_000f0bd99.png",
    "bone":"ID_00ed02fcc.png",
    "heatmap":"ID_00dfe0c88.png",
    "probabilidade":0.99
      }


// ordena os slices do com maior probabilidade de ter hemorragia para o que tem menos.      
function ordenena_slices(lista_de_slices){
    const chaves_slices = []
    //adiciona as chaves do json com os slices 
    for(chave in lista_de_slices){
        chaves_slices.push(chave)}
     for(i in chaves_slices){
        for(j in chaves_slices){ 
             if(lista_de_slices[(chaves_slices[i])]["probabilidade"] < lista_de_slices[(chaves_slices[j])]["probabilidade"]){
                var aux=chaves_slices[i]
                console.log(aux)
                chaves_slices.splice(i,1, chaves_slices[j])
                chaves_slices.splice(j,1, chaves_slices[aux])
                
                
            } 
            
        }console.log(chaves_slices )
    }
    return chaves_slices
}
ordenena_slices(lista_de_slices)

 
function mudarimg(obj, novaimg){
    document.getElementById(obj).src = novaimg; 

};



function ler_json(arquivo){
    var lista = require([arquivo])
    
    console.log(  lista)
     return lista

};
function set_imagem_atual2(){
     const nome_imagem=lista.imagem_att;
    return nome_imagem;
 


}


function set_imagem_atual(){
    const imagem_att=lista.imagem_att;
    const div = document.querySelector("#imagem_atual");
    mudarimg("imagem_atual",imagem_att)

}

function set_bone(arquivo){
    const bone=lista.bone;
    mudarimg("imagem_mod",bone)
    
       

}

function set_brain(){
    const brain=lista.brain;
    const botton =document.querySelector("#botton_brain");
    mudarimg("imagem_mod",brain)
    
       
}
function set_subdural(arquivo){
    const subdural=lista.subdural;
    mudarimg("imagem_mod",subdural)
}
function set_heatmap(arquivo){
    const heatmap=lista.heatmap;
    mudarimg("imagem_mod",heatmap)
}
 