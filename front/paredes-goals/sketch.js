var goals;
var fields = {};
var s = 15;
var p = 20;
var popupActive = false;
var criteria = ['AÑO', 'PELOTAS DETENIDAS', 'CLUB', 'RIVAL', 'ARQUERO', 'LOCAL O VISITA', 'TORNEO','PARTE DEL CUERPO', 'ESTADIO', 'ZONA DE LA CANCHA','RESULTADO'];
var Por = ['AÑO', 'CLUB', 'RIVAL', 'ARQUERO', 'LOCAL O VISITA', 'TORNEO', 'ESTADIO', 'RESULTADO', 'PARTE DEL CUERPO', 'ZONA DE LA CANCHA', 'PELOTAS DETENIDAS'];
var selection = null;
var drag = 0;
var x = 0,
  y = 0;
var closeButtonY = null;
var firstTouch = .5;

function dateString(date) {
  var d = date.substring(3,5), m = date.substring(0,2), y = date.substring(6,11);
  var months = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
  return d+" de "+months[int(m)-1]+" de "+y;
}

function resultString(resultado) {
  var result2 = resultado.substring(resultado.length-1,resultado.length);
  var team1 = resultado
  var team2 = resultado
  return resultado;
}

function popup(g) {
  var goal = goals[g];
  var y = goal.y + s;
  var h = 100;
  push();
  translate(0,-h-40);
  // background
  noStroke(); var opacity = 240;
  if (goal.CLUB == "Colo Colo") fill(224,50,50,opacity);
  else fill(135,opacity);
  rect(10, y, width-20, h,5,5,5,5);
  triangle(goal.x-10,y+h,goal.x+10,y+h,goal.x,y+h+s)
  // Text
  y += s*1.8;
  textSize(s*1.8), textAlign(CENTER), fill('white'), noStroke();
  text('Gol Número ' + goal['NRO DE GOL__1'], width/2, y);
  y += s*1.5;
  textSize(s*1.2);
  text(dateString(goal['FECHA']), width/2, y);
  y += s*1.5;
  textSize(s);
  //if (goal['LOCAL'] === 'Local') text(goal['CLUB'] + ' vs. ' + goal['RIVAL'], width/2, y);
  //else text(goal['RIVAL'] + ' vs. ' + goal['CLUB'], width/2, y);
  text(goal['RESULTADO__1'], width/4, y);
  text("Estadio "+ goal['ESTADIO'], width*.75, y);
  y += s*1.2;
  fill('white'),  textAlign(CENTER), textSize(s);
  text("Minuto "+ goal['Minuto'], width/4, y);
  text(goal['PARTE DEL CUERPO'], width*.75, y);
  //text(goal['PARTE DEL CUERPO'] + ' desde\n' + goal['ZONA DE LA CANCHA'], width*.75, y);
  stroke('white'),strokeWeight(1);
  line(width/2,y-s*2,width/2,y);


  pop();
  // Show selected goal
  if (goals[g].CLUB ==='Colo Colo')  fill('red'); else fill('black');
  noStroke(), ellipse(goals[g].x, goals[g].y, s-6, s-6);
  // Close button
  stroke('white'), strokeWeight(2);
  closeButtonY = goals[g].y-h-15;
  line(width-20,closeButtonY,width-25,closeButtonY+5);
  line(width-25,closeButtonY,width-20,closeButtonY+5);
}

function preload() {
  goals = loadJSON('paredes214.json');
  fontL = loadFont('Fonts/Teko/Teko-Light.ttf');
  fontM= loadFont('Fonts/Teko/Teko-Medium.ttf');
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  pixelDensity(2);
  textFont(fontM);

  /* Generate inverted index */
  for (var f in goals['1']) {
    var field = f;
    fields[field] = {};
    for (var g in goals) {
      var value = goals[g][field];
      if (!fields[field][value]) fields[field][value] = [];
      fields[field][value].push(g);
    }
  }
  /* Initialize ball positions */
  for (var g in goals) {
    goals[g].x = width/2;
    goals[g].y = 100;
  }
  Por = 'AÑO';
}

function drawTitle() {
  textFont('Helvetica'), textSize(r / 2), textAlign(CENTER), fill('red'), noStroke();
  text('216', 0, r / 6);
  textFont('arial narrow'), textSize(r / 6), strokeWeight(.5), stroke('white'), fill('black'), textStyle(BOLD);
  text('LOS GOLES\nDE PAREDES', 0, -r / 15 + 3);
}

function drawField() {
   stroke('grey'),noFill(), strokeWeight(3);
  /* Draw side lines */ //line(0,0,0,height), line(width,0,width,height);
  /* Draw half-way line */line(-width / 2, 0, width / 2, 0);
  /* Draw center circle */ellipse(0, 0, r, r);
  ellipse(0,0,4,4);
}

function menu() {
  r = 150;
  push();
  translate(width / 2, r / 1.2);
  drawField();

  textSize(r/9);
  for (var i in criteria) {
    var rotation = (i / criteria.length + drag) * TWO_PI + PI/2 + sin(frameCount/80)/firstTouch;
    textSize(r / 10), textStyle(NORMAL), textAlign(CENTER), strokeWeight(3);
    x = r * cos(rotation);
    y = r / 1.5 * sin(rotation) + 5;
    if (Por === criteria[i]) noStroke(), fill('red'), text('POR '+criteria[i], x, y+15);
    else fill(0,0,0,100), stroke('white'), text(criteria[i], x, y);
  }
  pop();
}

function draw() {
  clear();
  menu();
  var width2 = width-s*4;
  var height2 = 260 + s;
  var block = width2;
  var rowLeading = s*2;
  var blockLeading = s*2;
  keysSorted = Object.keys(fields[Por]).sort(function(a, b) {
    return Object.keys(fields[Por][b]).length - Object.keys(fields[Por][a]).length;
  })
  if (Por === 'AÑO') keysSorted = Object.keys(fields[Por]);
  for (var value in keysSorted) { //TODO order by frequency
    value = keysSorted[value];
    if (value) {
      textSize(s), textAlign(LEFT), fill('grey'), noStroke(), textStyle(BOLD);
      var nameWidth = textWidth(value);
      /* Draw value name */ text(value, (width-width2)/3, height2+2);
      textSize(s), textAlign(LEFT), fill('black'), textStyle(NORMAL);
     /* Draw goal count for value name */ text(Object.keys(fields[Por][value]).length, nameWidth + (width-width2)/2, height2 + 2);
      height2 += s;
      sx = s + s / 2;
      var capacity = int(block / sx)+1;
      for (var g in fields[Por][value]) {
        var goal = goals[fields[Por][value][g]];

        if (goal.Por !== null) {
          goal['ty'] = height2 + int(g / capacity) * rowLeading;
          goal['tx'] = (width-width2)/2 + g * sx - sx * capacity * int(g / capacity) - 2; // margin+xPos+yCorrection+optiCorrection
        }
        else goal['ty'] = -500, goal['tx'] = -500; // Out of the screen
        goal['x'] = lerp(goal.x, goal.tx, .15);
        goal['y'] = lerp(goal.y, goal.ty, .15);

        noFill(), strokeWeight(4);
        if (goal.CLUB === 'Colo Colo') stroke(255, 0, 0);
        else stroke('black');
        ellipse(goal.x, goal.y, s, s);
      }
      height2 += int(Object.keys(fields[Por][value]).length / capacity) * rowLeading + blockLeading;
      if (Object.keys(fields[Por][value]).length % capacity == 0) height2 -= rowLeading;
    }
  }
  if (height2 > height || height2 < (height-500)) {
    resizeCanvas(width, height2);
    //print(height);
  }
  if (selection) popup(selection);
}


function mousePressed() {
  //if (selection && abs(mouseY - goals[selection].y) < 6 && abs(mouseX - goals[selection].x) < 6) {
  if (selection && abs(mouseY - closeButtonY-2.5) < 8 && abs(mouseX - width+22.5) < 8 ) {
    selection = null;
  } else {
    for (var g in goals) {
      if (abs(mouseX - goals[g].x) < s / 2 + 2 && abs(mouseY - goals[g].y) < s / 2 + 2) {
        print(goals[g]['NRO DE GOL__1']);
        selection = g;
        popup(selection);
      }
    }
  }
  // Menu demo spin
  if (mouseY > 20) firstTouch = 20;
}

function mouseDragged() {
  var dragForce = .005;
  if (mouseY < 250) {
    if ((pmouseY <= mouseY && mouseX > width/2) || (pmouseY >= mouseY && mouseX < width/2)) drag += dragForce;
    else drag -= dragForce;
    var phase = - .6;
    if (drag < 0) phase = -phase;
    var i = int(-drag * 11 +phase) % criteria.length;
    if (i < 0) i += criteria.length;
    Por = criteria[i];
    return false;
  }
}
