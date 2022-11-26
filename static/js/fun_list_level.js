
var curFieldNameId = 1;
let listOfFields = [];

function sendFormLyrix(){
    var string_list_level = []
    for (index = 0; index < listOfFields.length; ++index) {
        var data_input_level = document.getElementById(listOfFields[index]);
        string_list_level.push("'" + data_input_level.value + "'");
    }
    format_list_level = '[' + string_list_level.join() + ']';
    if(confirm('Вы уверены?')){
        document.sendform.LYRIX_ACCESS_LEVELS.value = format_list_level;
        return true;}
    return false;
 }

function addField(e){
     var keyBox = document.sendform.add_level;
     var val = keyBox.value;
     if(val.length<1){
         return;
     }
     var div = document.createElement("div");
     curFieldNameId++;
     div.innerHTML = "<p><input id=\"name_" + curFieldNameId + "\"  value=\"" + val + "\" type=\"text\" required size=\"50\" /> <input type=\"button\" name=\"" + curFieldNameId + "\" onclick=\"return deleteField(this)\" value=\"Удалить\" /><p>";
     listOfFields.push("name_"  + curFieldNameId);
     document.getElementById("addLevelId").appendChild(div);
     // Возвращаем false, чтобы не было перехода по сслыке
     return false;
}

function deleteField(a) {
         // Получаем доступ к ДИВу, содержащему поле
         var contDiv = a.parentNode;
         // Удаляем этот ДИВ из DOM-дерева
         contDiv.parentNode.removeChild(contDiv);
         // Уменьшаем значение текущего числа полей
         var find_name="name_"+a.name
         for (index = 0; index < listOfFields.length; ++index) {
            if (listOfFields[index] == "name_"+a.name){
                listOfFields.splice(index,1);
                break
            }
         }
         curFieldNameId--;
         // Возвращаем false, чтобы не было перехода по сслыке
         return false;
}

function createListLevel(){
        var list_level = document.sendform.LYRIX_ACCESS_LEVELS.value;
        var arrayOfStrings = list_level.split(',');
        var index;
        for (index = 0; index < arrayOfStrings.length; ++index) {
             var div = document.createElement("div");
             curFieldNameId++;
             div.innerHTML = "<p><input id=\"name_" + curFieldNameId + "\"  value=\"" + arrayOfStrings[index] + "\" type=\"text\" required size=\"50\" /> <input type=\"button\" name=\"" + curFieldNameId + "\" onclick=\"return deleteField(this)\" value=\"Удалить\" /><p>";
             listOfFields.push("name_" + curFieldNameId);
             // Добавляем новый узел в конец списка полей
             document.getElementById("addLevelId").appendChild(div);
             // Возвращаем false, чтобы не было перехода по сслыке
         }
         return false;
}

window.onload = createListLevel;
//var sendButton = document.sendform.send;
//sendButton.addEventListener("click", sendFormLyrix);
var addLevelButton = document.sendform.button_add;
addLevelButton.addEventListener("click", addField);