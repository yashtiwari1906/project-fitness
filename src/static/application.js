
// $(document).ready(function(){
//     //connect to the socket server.
//     var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
//     var numbers_received = [];

//     //receive details from server
//     socket.on('newnumber', function(msg) {
//         console.log("Received number" + msg.reps);
//         //maintain a list of ten numbers
//         console.log("value is being recienved"+ msg);
//         numbers_received.push(msg.number);
//         numbers_string = '';
//         for (var i = 0; i < numbers_received.length; i++){
//             numbers_string = numbers_received[i].toString();
//         }
//         console.log("number string is: "+numbers_string)
//         $('#log').html(numbers_string);
//     });

// });




$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        //console.log("Received number" + msg.reps.toString());
        //maintain a list of ten numbers
        // if (numbers_received.length >= 10){
        //     numbers_received.shift()
        // }            
        // numbers_received.push(msg.number);
        // numbers_string = '';
        // for (var i = 0; i < numbers_received.length; i++){
        //     numbers_string = numbers_received[i].toString();
        // }
        $('#log').html(msg.reps.toString());
    });

});