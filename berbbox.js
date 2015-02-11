var Mbox = require('node-mbox');
var berbbox    = new Mbox('Berb.mbox', { /* options */ });
var MailParser = require("mailparser").MailParser


var emails = [];



function not_history(line){
	return line.length > 0 && line[0] != '>'
}

//RETURNS frequency table of words found in emails
function emails_frequency( emails ){
	var word_freq = {};
	emails.forEach(function(email){
		email_word_freq(email, word_freq);
	});
	return word_freq;
}

//MUTATES freq_table based on words found in email
function email_word_freq(email, freq_table){
	var email_split = email.split(' ');
	email_split.forEach(function(email_word){
		if(freq_table[email_word]){
			freq_table[email_word] += 1;
		}
		else{
			freq_table[email_word] = 1;
		}
	});
}

function no_quotes(a_string){
	var ret_string = "";
	for(var i =0; i<a_string.length; i++){
		if( a_string[i] != '"'){
			ret_string += a_string[i];
		}
	}
	return ret_string;
}


// Next, catch events generated: 
berbbox.on('message', function(msg) {
	var mailparser = new MailParser();
	mailparser.on("end", function(parsed_mail){
		if( parsed_mail.text ){
			var no_hist = parsed_mail["text"].split('\n').filter(not_history);
			emails.push(no_hist.join(' '));
		}
	});


    mailparser.write(msg);
    mailparser.end();
});

var fs = require('fs');
var file_out = fs.createWriteStream('refined.js');
file_out.write("berb_text = [")

berbbox.on('end', function() {
	console.log("done", emails.length);
	var freq_table = emails_frequency(emails);
	var berb_table = {}

	console.log(freq_table[0]);

	Object.keys(freq_table).forEach(function(key){

		if(  key.toLowerCase().indexOf("berb") > -1){
			berb_table[key] = freq_table[key]
			var key = no_quotes(key);
			file_out.write('"'+key+'",')
		}
	});
	console.log(berb_table)
	file_out.write('"Happy Valentine\'s Day Berb!"]');
	file_out.end();
});

