lista={ "imagem_att": "ID_000f0bd99.png",
    "brain":"ID_00fdec745.png",
    "subdural":"ID_000f0bd99.png",
    "bone":"ID_00ed02fcc.png",
    "heatmap":"ID_00fdec745.png"
      }







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
 