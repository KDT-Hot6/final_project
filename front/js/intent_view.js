function minus_click(dom){
	tr = dom.parentElement.parentElement;
	var i = dom.parentElement.getAttribute("rowspan");
	if(i){
		for(var j =1; j < i; j++){
			tmp = tr;
			while(1){
				tmp = tmp.nextSibling;
				if(tmp.nodeName == "TR"){
					break;
				}
			}
			clear_node(tmp);
		}
	}else{
		var cnt = 0;
		var rowspan = 0;
		var tmp = tr;
		var flag = true;
		var node = null;
		while(flag){
			cnt += 1;
			children = tmp.childNodes;
			for(var k = 0; k < children.length; k++ ){
				if(children[k].nodeType != 1) {
					continue;
				}
				node = children.item(k);
				if(node.getAttribute("rowspan")){
					rowspan = node.getAttribute("rowspan");
					node = tmp; //여기서 node가 tr이 됨
					flag = false;
				}
				break;
			}
			while(flag){
				tmp = tmp.previousSibling;
				if(tmp.nodeType != 1){
					continue;
				}
				break;
			}
		}
		if(cnt == 1){ //나 혼자면 밑에 로직 수행안하고 그냥 삭제			
			var nt = find_next_sibling(tr,"TR"); //내가 이 테이블의 마지막 행이면 서치가 안됨
			if(nt != null && !find_children(nt,"TD",true).getAttribute("rowspan")){
				var s = '<td rowspan="'+(rowspan -1)+'"><button class="minus-btn" onclick="minus_click(this)">-</button><button class="plusBtn" onclick="click_plus(this)">+</button></td>';
				s += '<td rowspan="'+(rowspan -1)+'"><input type="text" value="'+tr.getElementsByTagName("INPUT")[0].value +'" /></td>';
				nt.innerHTML = s + nt.innerHTML.replace("<textarea></textarea>","<textarea>"+find_children(find_children(nt,"TD",true),"TEXTAREA",true).value+"</textarea>");				
			}
		}else{
			node_child = node.childNodes;
			var b = -1;
			var c = 0;
			while(c < 2){
				b += 1;
				if(node_child[b].nodeType != 1){
					continue;
				}
				if(node_child[b].getAttribute("rowspan")){
					node_child[b].setAttribute("rowspan", rowspan -1);
					c += 1;
				}
			}
		}
	}
	clear_node(tr);
	show_plus_btn();
// 				if(children[i].nodeType == 1){
// 	alert(tbody.firstChild);
// 	var i = dom.parentElement.getAttribute("rowspan");
	
// 	while(elem.hasChildNodes()){
// 		elem.removeChild(elem.lastChild);
// 	}
// 	elem.remove();
// 	dom.parentElement.parentElement.remove();
}

function click_plus(dom){
	tr = dom.parentElement.parentElement;
	var rowspan = dom.parentElement.getAttribute("rowspan");
	var tb = document.getElementsByTagName("TBODY")[0];
	if(rowspan){		
		//테이블의 마지막에 추가 새로운 tr 추가 rowspan=1
// 		tb.innerHTML += '<tr><td rowspan="1"><button class="minus-btn" onclick="minus_click(this)">-</button> <button class="plusBtn" onclick="click_plus(this)">+</button></td> <td rowspan="1"><input type="text"></input></td> <td><textarea></textarea></td> <td><button class="minus-btn" onclick="minus_click(this)">-</button><button class="plusBtn" onclick="click_plus(this)">+</button></td></tr>'
		var tr = document.createElement("TR");
		var td1 = document.createElement("TD");
		var td2 = document.createElement("TD");
		var td3 = document.createElement("TD");
		var td4 = document.createElement("TD");
		var td5 = document.createElement("TD");
		var ip = document.createElement("INPUT");
		var ta = document.createElement("TEXTAREA");
		var btn1 = document.createElement("BUTTON");
		var btn2 = document.createElement("BUTTON");
		var btn3 = document.createElement("BUTTON");
		var btn4 = document.createElement("BUTTON");
		var t1 = document.createTextNode("-");
		var t2 = document.createTextNode("+");
		var t3 = document.createTextNode("-");
		var t4 = document.createTextNode("+");
		var sel = document.createElement("SELECT");
		var o1 = document.createElement("OPTION");
		var o2 = document.createElement("OPTION");
		o2.setAttribute("selected", true);
		var o3 = document.createElement("OPTION");
		var o4 = document.createElement("OPTION");
		var o5 = document.createElement("OPTION");
		var o6 = document.createElement("OPTION");
		var ot1 = document.createTextNode("1");
		var ot2 = document.createTextNode("2");
		var ot3 = document.createTextNode("3");
		var ot4 = document.createTextNode("4");
		var ot5 = document.createTextNode("5");
		var ot6 = document.createTextNode("6");

		//option설정
		o1.value = "1";
		o2.value = "2";
		o3.value = "3";
		o4.value = "4";
		o5.value = "5";
		o6.value = "6";
		
		o1.appendChild(ot1);
		o2.appendChild(ot2);
		o3.appendChild(ot3);
		o4.appendChild(ot4);
		o5.appendChild(ot5);
		o6.appendChild(ot6);

		sel.appendChild(o1);
		sel.appendChild(o2);
		sel.appendChild(o3);
		sel.appendChild(o4);
		sel.appendChild(o5);
		sel.appendChild(o6);
		
		//td1,2 는 rowspan 설정 필요
		td1.setAttribute("rowspan", "1");
		td2.setAttribute("rowspan", "1");

		//ip type
		ip.setAttribute("type", "text");

		//btn1,2도 class onclick등 추가
		btn1.setAttribute("class", "minus-btn");
		btn1.setAttribute("onclick", "minus_click(this)");
		btn1.appendChild(t1);

		btn2.setAttribute("class", "plusBtn");
		btn2.setAttribute("onclick", "click_plus(this)");
		btn2.appendChild(t2);

		btn3.setAttribute("class", "minus-btn");
		btn3.setAttribute("onclick", "minus_click(this)");
		btn3.appendChild(t3);

		btn4.setAttribute("class", "plusBtn");
		btn4.setAttribute("onclick", "click_plus(this)");
		btn4.appendChild(t4);

		td1.appendChild(btn1);
		td1.appendChild(btn2);
		tr.appendChild(td1);

		td2.appendChild(ip);
		tr.appendChild(td2);

		td3.appendChild(ta);
		tr.appendChild(td3);

		td4.appendChild(sel);
		tr.appendChild(td4);
		
		td5.appendChild(btn3);
		td5.appendChild(btn4);
		tr.appendChild(td5);
		
		tb.appendChild(tr);
	}else{
		//1.rowspan값을 가지고 있는 td를 가지고 있는 tr 가져오기
// 		alert(tr);
		var cnt = 0;
		var rowspan = 0;
		var tmp = tr;
		var flag = true;
		var node = null;
		while(flag){
			cnt += 1;
			children = tmp.childNodes;
			for(var k = 0; k < children.length; k++ ){
				if(children[k].nodeType != 1) {
					continue;
				}
				node = children.item(k);
				if(node.getAttribute("rowspan")){
					rowspan = parseInt(node.getAttribute("rowspan"));
					node = tmp; //여기서 node가 tr이 됨
					flag = false;
				}
				break;
			}
			while(flag){
				tmp = tmp.previousSibling;
				if(tmp.nodeType != 1){
					continue;
				}
				break;
			}
		}
// 		while(1){
// 			if(str.getAttribute("rowspan")){
// 				break;		
// 			}else{
// 				str = find_prev_sibling(str,"TR");
// 			}
// 		}
		
		var tds = node.getElementsByTagName("TD");	
		//2.td 2개 rowspan 바꾸고
		for(var i = 0;i<2; i++){
// 			alert(tds[i].getAttribute("rowspan"));
			tds[i].setAttribute("rowspan", rowspan+1);
		}
		//3.현재 tr의 다음 형제로 추가
		var ltr = document.createElement("TR");
		var td1 = document.createElement("TD");
		var td2 = document.createElement("TD");
		var ta = document.createElement("TEXTAREA");
		var btn1 = document.createElement("BUTTON");
		var btn2 = document.createElement("BUTTON");
		var t1 = document.createTextNode("-");
		var t2 = document.createTextNode("+");
// 		var t3 = document.createTextNode("append");

		var td3 = document.createElement("TD");
		var sel = document.createElement("SELECT");
		var o1 = document.createElement("OPTION");
		var o2 = document.createElement("OPTION");
		var o3 = document.createElement("OPTION");
		var o4 = document.createElement("OPTION");
		var o5 = document.createElement("OPTION");
		var o6 = document.createElement("OPTION");
		var ot1 = document.createTextNode("1");
		var ot2 = document.createTextNode("2");
		var ot3 = document.createTextNode("3");
		var ot4 = document.createTextNode("4");
		var ot5 = document.createTextNode("5");
		var ot6 = document.createTextNode("6");

		//option설정
		o1.value = "1";
		o2.value = "2";
		o3.value = "3";
		o4.value = "4";
		o5.value = "5";
		o6.value = "6";
		
		o1.appendChild(ot1);
		o2.appendChild(ot2);
		o2.setAttribute("selected", true);
		o3.appendChild(ot3);
		o4.appendChild(ot4);
		o5.appendChild(ot5);
		o6.appendChild(ot6);

		sel.appendChild(o1);
		sel.appendChild(o2);
		sel.appendChild(o3);
		sel.appendChild(o4);
		sel.appendChild(o5);
		sel.appendChild(o6);
		
		
		btn1.setAttribute("class", "minus-btn");
		btn1.setAttribute("onclick", "minus_click(this)");
		btn1.appendChild(t1);

		btn2.setAttribute("class", "plusBtn");
		btn2.setAttribute("onclick", "click_plus(this)");
		btn2.appendChild(t2);

// 		ta.appendChild(t3);
		td1.appendChild(ta);
		ltr.appendChild(td1);

		td2.appendChild(sel);
		ltr.appendChild(td2);

		td3.appendChild(btn1);
		td3.appendChild(btn2);
		ltr.appendChild(td3);
		
		//우선 tbody에 추가를 해두고, 현재 tr의 다음 tr에 insert before 그런데 마지막이면 그냥 tbody에 추가
		if(find_next_sibling(tr,"TR")){
// 			find_next_sibling(tr,"TR").appendChild(t3);
			tb.insertBefore(ltr,find_next_sibling(tr,"TR"));
		}else{
			tb.appendChild(ltr);				
		}
		
	}
	show_plus_btn();
}

function show_plus_btn(){
	
	//우선 모든 plusBtn을 안보이게함.
	var x = document.getElementsByClassName('plusBtn');
	for (var i = 0; i < x.length; i++) {
		  x[i].style.display = 'none';
	}
	
	var tr_list = document.getElementsByTagName('TR');
	var len = tr_list.length;
// 	for(var i = 0; i < len; i++){
// 		tr_list[i]
// 	}
	var i = 0;
	var rowspan = 0;
	
	while(1){		
		
		var td = find_children(tr_list[i],"TD",true);
		rowspan = parseInt(td.getAttribute("rowspan"));
// 		alert(td.lastChild.nodeName);
// 		break;
		var t = find_children(tr_list[i+rowspan-1],"TD",false).lastChild;
		t.style.display = 'inline';		
		if(i+rowspan == len){
// 			td.lastChild.innerHTML = 'block';
			td.lastChild.style.display = 'inline';
// 			alert(td.lastChild);
// 			alert(td.lastChild.innerHTML)
			break;
		}
		i += rowspan;
	}

}

function find_children(n,tnn,f){ //n = node 객체, tnn = 타겟노드네임 , f 플래그 트루면 첫번째 펄스면 마지막
	var tmp = n.childNodes;
	if(f){
		for(var i =0; i < tmp.length; i++ ){
			if(tmp[i].nodeType != 1){
				continue;
			}
			if(tmp[i].nodeName == tnn){
				return tmp[i];
			}
		}		
	}else{
		for(var i =tmp.length -1; i > -1 ; i-- ){
			if(tmp[i].nodeType != 1){
				continue;
			}
			if(tmp[i].nodeName == tnn){
				return tmp[i];
			}
		}				
	}
	return null;
}

function find_parent(n,tnn){
	var tmp = n.parentElement;
	while(1){
		if(tmp.nodeType == 1){
			if(tmp.nodeName == tnn){
				break;
			}
			if(tmp.nodeName == "BODY"){
				return null;
			}
		}
		tmp = tmp.parentElement;
	}
	return tmp;	
}

function find_next_sibling(n,tnn){ //형제가 없는 경우
	var tmp = n.nextSibling;
	while(1){
		if(tmp == null){
			return null;
		}
		if(tmp.nodeType == 1){
			if(tmp.nodeName == tnn){
				break;
			}
		}
		tmp = tmp.nextSibling;
	}
	return tmp;	
}

function find_prev_sibling(n,tnn){
	var tmp = n.previousSibling;
	var f = true;
	while(f){
		if(tmp.nodeType == 1){
			if(tmp.nodeName == tnn){
				alert("while"+tmp.nodeName);			
				f = false;
				break;
			}
		}
		tmp = tmp.previousSibling;
	}
	alert(tmp);
	return tmp;	
}

function clear_node(elem){
	while(elem.hasChildNodes()){
		elem.removeChild(elem.lastChild);
	}
	elem.remove();
}