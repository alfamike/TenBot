# This Python file uses the following encoding: utf-8
'''
Created on 28 mar. 2018

@author: Alvaro
'''
import telebot
import pysnmp

TOKEN= "583704103:AAEiWiGV2XxMzRNDJGiJ2FSseR4InXB_un8"
bot= telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    cid= message.chat.id
    start_message= "Bienvenido al bot de Gestión del Grupo 10"
    bot.send_message(cid, start_message)

@bot.message_handler(commands=['stats'], content_types=['text'])
def stats_handler(message):
    f= open('../tmp/prueba.html','w')
    pagina= '''<!DOCTYPE HTML><html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      // Load the Visualization API and the corechart package.
      google.charts.load('current', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Topping');
        data.addColumn('number', 'Slices');
        data.addRows([
          ['Mushrooms', 3],
          ['Onions', 1],
          ['Olives', 1],
          ['Zucchini', 1],
          ['Pepperoni', 2]
        ]);

        // Set chart options
        var options = {'title':'How Much Pizza I Ate Last Night',
                       'width':400,
                       'height':300};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <div id="chart_div"></div>
  </body>
</html>'''
    f.write(pagina)
    f.close()

    f= open('../tmp/prueba.html','r')
    cid= message.chat.id
    bot.send_document(cid,f)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
bot.polling()