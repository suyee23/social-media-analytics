// config.js
module.exports = {
    consumer_key:         '...',
    consumer_secret:      '...',
    access_token:         '...',
    access_token_secret:  '...',
  
 }

 // bot.js
 var Twit = require ('twit');
 
var config = require('./config')
var T = new Twit(config);
 
var params = {q: 'coronavirus', count: 100, lang: 'en'}
 
T.get('search/tweets', params, gotData);
 
function gotData (err, data, response) {
   for (var i in data.statuses) {
       tweet = (data.statuses[i].text)
 
       var str = tweet;
 
      // remove RT @account
      var str  = str.replace(/RT\s*@\S+/g, '');
     
      // remove URL
      var str = str.replace(/(?:https?|ftp):\/\/[\n\S]+/g, '');
 
      // convert to lowercase
      var str = str.toLowerCase()
 
      // remove special characters
      var str = str.replace(/[^a-zA-Z ]/g, "");
     
      // remove stop words
      var stopwords = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself',
      'yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them',
      'their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are',
      'was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the',
      'and','but','if','or','because','as','until','while','of','at','by','for','with','about','against',
      'between','into','through','during','before','after','above','below','to','from','up','down','in','out',
      'on','off','over','under','again','further','then','once','here','there','when','where','why','how','all',
      'any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so',
      'than','too','very','s','t','can','will','just','don','should','now'];
     
      function remove_stopwords(str) {
          res = []
          words = str.split(' ')
          for(i=0;i<words.length;i++) {
              word_clean = words[i].split(".").join("")
              if(!stopwords.includes(word_clean)) {
                  res.push(word_clean)
               }
           }
           return(res.join(' '))
       };
      
       var str = remove_stopwords(str);
      
       // remove extra empty white spaces
       var str = str.replace(/\s+/g, ' ').trim();
      
       console.log(str);
   }
};
