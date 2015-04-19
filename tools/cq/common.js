//document.domain = 'uicms.net';  
var BROWSER = {};
var disallowfloat='reg';
var USERAGENT = navigator.userAgent.toLowerCase();
browserVersion({'ie':'msie','firefox':'','chrome':'','opera':'','safari':'','mozilla':'','webkit':'','maxthon':'','qq':'qqbrowser'});
if(BROWSER.safari)
{
	BROWSER.firefox = true;
}
BROWSER.opera = BROWSER.opera ? opera.version() : 0;
HTMLNODE = document.getElementsByTagName('head')[0].parentNode;
if(BROWSER.ie)
{
	BROWSER.iemode = parseInt(typeof document.documentMode != 'undefined' ? document.documentMode : BROWSER.ie);
	HTMLNODE.className = 'ie_all ie' + BROWSER.iemode;
}

var CSSLOADED = [];
var JSLOADED = [];
var JSMENU = [];
JSMENU['active'] = [];
JSMENU['timer'] = [];
JSMENU['drag'] = [];
JSMENU['layer'] = 0;
JSMENU['zIndex'] = {'win':200,'menu':300,'dialog':400,'prompt':500};
JSMENU['float'] = '';


var EXTRAFUNC = [];
EXTRAFUNC['showmenu'] = [];
var NOTICETITLE = [];

if(BROWSER.firefox && window.HTMLElement)
{
	HTMLElement.prototype.__defineGetter__( "innerText", function(){
		var anyString = "";
		var childS = this.childNodes;
		for(var i=0; i <childS.length; i++)
		{
			if(childS[i].nodeType==1)
			{
				anyString += childS[i].tagName=="BR" ? '\n' : childS[i].innerText;
			}
			else if(childS[i].nodeType==3)
			{
				anyString += childS[i].nodeValue;
			}
		}
		return anyString;
	});
	HTMLElement.prototype.__defineSetter__( "innerText", function(sText){
		this.textContent=sText;
	});
	HTMLElement.prototype.__defineSetter__('outerHTML', function(sHTML) {
			var r = this.ownerDocument.createRange();
		r.setStartBefore(this);
		var df = r.createContextualFragment(sHTML);
		this.parentNode.replaceChild(df,this);
		return sHTML;
	});

	HTMLElement.prototype.__defineGetter__('outerHTML', function() {
		var attr;
		var attrs = this.attributes;
		var str = '<' + this.tagName.toLowerCase();
		for(var i = 0;i < attrs.length;i++)
		{
			attr = attrs[i];
			if(attr.specified)
			str += ' ' + attr.name + '="' + attr.value + '"';
		}
		if(!this.canHaveChildren)
		{
			return str + '>';
		}
		return str + '>' + this.innerHTML + '</' + this.tagName.toLowerCase() + '>';
		});

	HTMLElement.prototype.__defineGetter__('canHaveChildren', function() {
		switch(this.tagName.toLowerCase()) {
			case 'area':case 'base':case 'basefont':case 'col':case 'frame':case 'hr':case 'img':case 'br':case 'input':case 'isindex':case 'link':case 'meta':case 'param':
			return false;
			}
		return true;
	});
}

var imagemaxwidth = '195';var aimgcount = new Array();
var replyreload = '', attachimgST = new Array(), zoomgroup = new Array(), zoomgroupinit = new Array();
function attachimggroup(pid)
{
	if(!zoomgroupinit[pid])
	{
		for(i = 0;i < aimgcount[pid].length;i++)
		{
			zoomgroup['aimg_' + aimgcount[pid][i]] = pid;
		}
		zoomgroupinit[pid] = true;
	}
}


function $(id){return ui(id);}
function ui(id)
{
	return !id ? null : document.getElementById(id);
}

function tag_id(tag, obj)
{
	return (typeof obj == 'object' ? obj : ui(obj)).getElementsByTagName(tag);
}

function ui_class(classname, ele, tag)
{
	var returns = [];
	ele = ele || document;
	tag = tag || '*';
	
	if(ele.getElementsByClassName)
	{
		var eles = ele.getElementsByClassName(classname);
		if(tag != '*')
		{
			for (var i = 0, L = eles.length; i < L; i++)
			{
				if (eles[i].tagName.toLowerCase() == tag.toLowerCase())
				{
					returns.push(eles[i]);
				}
			}
		}
		else
		{
			returns = eles;
		}
	}
	else
	{
		eles = ele.getElementsByTagName(tag);
		
		var pattern = new RegExp("(^|\\s)"+classname+"(\\s|$)");
		for (i = 0, L = eles.length; i < L; i++)
		{
			if (pattern.test(eles[i].className))
			{
					returns.push(eles[i]);
			}
		}
	}
	return returns;
}

function _attachEvent(obj, evt, func, eventobj)
{
	eventobj = !eventobj ? obj : eventobj;
	if(obj.addEventListener)
	{
		obj.addEventListener(evt, func, false);
	}
	else if(eventobj.attachEvent)
	{
		obj.attachEvent('on' + evt, func);
	}
}

function _detachEvent(obj, evt, func, eventobj)
{
	eventobj = !eventobj ? obj : eventobj;
	if(obj.removeEventListener)
	{
		obj.removeEventListener(evt, func, false);
	}
	else if(eventobj.detachEvent)
	{
		obj.detachEvent('on' + evt, func);
	}
}

function browserVersion(types)
{
	var other = 1;
	for(i in types)
	{
		var v = types[i] ? types[i] : i;
		if(USERAGENT.indexOf(v) != -1)
		{
			var re = new RegExp(v + '(\\/|\\s)([\\d\\.]+)', 'ig');
			var matches = re.exec(USERAGENT);
			var ver = matches != null ? matches[2] : 0;
			other = ver !== 0 && v != 'mozilla' ? 0 : other;
		}
		else
		{
			var ver = 0;
		}
		eval('BROWSER.' + i + '= ver');
	}
	BROWSER.other = other;
}

function getEvent()
{
	if(document.all) return window.event;
	func = getEvent.caller;
	while(func != null)
	{
		var arg0 = func.arguments[0];
		if (arg0)
		{
			if((arg0.constructor  == Event || arg0.constructor == MouseEvent) || (typeof(arg0) == "object" && arg0.preventDefault && arg0.stopPropagation))
			{
				return arg0;
			}
		}
		func=func.caller;
	}
	return null;
}

function isUndefined(variable)
{
	return typeof variable == 'undefined' ? true : false;
}

function in_array(needle, haystack)
{
	if(typeof needle == 'string' || typeof needle == 'number')
	{
		for(var i in haystack)
		{
			if(haystack[i] == needle)
			{
					return true;
			}
		}
	}
	return false;
}

function ajax_login()
{
	showWindow('login', 'index.php?m=user&c=login&api=uicms', 'get',-1);	
	return false;	
}

function ajax_login_judge()
{
	showWindow('login', 'index.php?m=user&c=login&a=login_judge&api=uicms', 'get',-1);	
	return false;	
}


function isLogin(type)
{
	if(type=='ui')
	{
		appendscript('api/index.php?m=ajax&a=user_json&inajax=1&api=uicms');	
	}
	else	
	{
		appendscript('api/index.php?m=ajax&a=msg&inajax=1&api=uicms');	
	}
	return false;	
}


//显示广告
function get_ad(obj)
{
	ajaxget('index.php?api=uicms&m=index&c=ajax&a=uigg&id='+obj, 'adv_'+obj);
}

function soso()
{	
	list = ui('search').getElementsByTagName('input');		
	for(i = 0;i < list.length;i++)
	{
		if(list[i].name.match('radiobutton') && list[i].checked)
		{
			mod = list[i].value;
		}
	}
	
	if(!ui('k').value)
	{
		showError('请填写您要搜索的关键�?');
	}
	else
	{	
		
		from = site_url+'index.php?m=search&a=so&module='+mod+'&kw='+encodeURI(ui('k').value);		
		window.open(from);
	}
}
/*验证�?*/
function get_lg_num(o,width,height,type)
{	
	url = site_url+'index.php?m=index&c=ck';
	if(width)
	{
		url += '&width='+width;
	}	
	if(height)
	{
		url += '&height='+height;
	}	
	if(type)
	{
		//url += '&a='+type;
	}
	ui(o).src = hostconvert(url)+'&t='+Math.random();
}

function checkpost()
{	
	var uiuser = ui('uiuser');
	var uipw = ui('uipw');
	ispass=false;
	if(uiuser.value=="" || uiuser.value=="用户名或邮箱")
	{
		showError('请填写您的昵称或邮箱账号');
		return false;
	}
	if(uipw.value.length<6 || uipw.value=="12345")
	{
		showError('密码填写错误');		
		return false;
	}
	ispass=true;
}

function is_register()
{	
	ispass=true;
}

// 登陆点击提交按钮之后
function lsSubmit(op,is_reg)
{
	is_reg ? is_register() : checkpost();
	if(ispass)
	{		
		ajaxpost('lsform', 'return_ls', 'return_ls','','1');
	}
	else
	{
		return false;
	}
}

function ui_ajax(url,data,recall)
{
	var ptype = !data || isUndefined(data) ? false : true;	
	var x = new Ajax();	
	x.recvType = 'JSON';
	if(ptype==true)
	{
		x.post(url, data, function(data, x)
		{
			if (recall && typeof recall === "function")
			{
				recall(data);
			}
		
		});	
	}
	else
	{
		x.getJSON(url, function(data, x)
		{
			if (recall && typeof recall === "function")
			{
				recall(data);
			}	
		});	
	}
}

function trim(str) {
	return (str + '').replace(/(\s+)$/g, '').replace(/^\s+/g, '');
}

function strlen(str) {
	return (BROWSER.ie && str.indexOf('\n') != -1) ? str.replace(/\r?\n/g, '_').length : str.length;
}

function mb_strlen(str) {
	var len = 0;
	for(var i = 0; i < str.length; i++) {
		len += str.charCodeAt(i) < 0 || str.charCodeAt(i) > 255 ? (charset == 'utf-8' ? 3 : 2) : 1;
	}
	return len;
}


//替换
function preg_replace(search, replace, str, regswitch) {
	var regswitch = !regswitch ? 'ig' : regswitch;
	var len = search.length;
	for(var i = 0; i < len; i++) {
		re = new RegExp(search[i], regswitch);
		str = str.replace(re, typeof replace == 'string' ? replace : (replace[i] ? replace[i] : replace[0]));
	}
	return str;
}

//HTML字符替换
function htmlspecialchars(str)
{
	return preg_replace(['&', '<', '>', '"'], ['&amp;', '&lt;', '&gt;', '&quot;'], str);
}

//URL字符替换
function URLspecialchars(str)
{
	return preg_replace(['&amp;'], ['&'],  str);
}

//隐藏 显示 切换
function display(id)
{
	var obj = ui(id);
	if(obj.style.visibility)
	{
		obj.style.visibility = obj.style.visibility == 'visible' ? 'hidden' : 'visible';
	}
	else
	{
		obj.style.display = obj.style.display == '' ? 'none' : '';
	}
}
//全�?
function checkall(form, prefix, checkall) {
	var checkall = checkall ? checkall : 'chkall';
	count = 0;
	for(var i = 0; i < form.elements.length; i++) {
		var e = form.elements[i];
		if(e.name && e.name != checkall && !e.disabled && (!prefix || (prefix && e.name.match(prefix)))) {
			e.checked = form.elements[checkall].checked;
			if(e.checked) {
				count++;
			}
		}
	}
	return count;
}

function Ajax(recvType, waitId)
{

	var aj = new Object();
	aj.loading = '请稍�?...';
	aj.recvType = recvType ? recvType : 'XML';
	aj.waitId = waitId ? $(waitId) : null;
	aj.resultHandle = null;
	aj.sendString = '';
	aj.targetUrl = '';

	aj.setLoading = function(loading)
	{
		if(typeof loading !== 'undefined' && loading !== null) aj.loading = loading;
	};

	aj.setRecvType = function(recvtype)
	{
		aj.recvType = recvtype;
	};

	aj.setWaitId = function(waitid)
	{
		aj.waitId = typeof waitid == 'object' ? waitid : $(waitid);
	};

	aj.createXMLHttpRequest = function()
	{
		var request = false;
		if(window.XMLHttpRequest)
		{
			request = new XMLHttpRequest();
			if(request.overrideMimeType)
			{
				request.overrideMimeType('text/xml');
			}
		}
		else if(window.ActiveXObject)
		{
			var versions = ['Microsoft.XMLHTTP', 'MSXML.XMLHTTP', 'Microsoft.XMLHTTP', 'Msxml2.XMLHTTP.7.0', 'Msxml2.XMLHTTP.6.0', 'Msxml2.XMLHTTP.5.0', 'Msxml2.XMLHTTP.4.0', 'MSXML2.XMLHTTP.3.0', 'MSXML2.XMLHTTP'];
			for(var i=0; i<versions.length; i++)
			{
				try
				{
					request = new ActiveXObject(versions[i]);
					if(request)
					{
						return request;
					}
				} catch(e) {}
			}
		}
		return request;
	};

	aj.XMLHttpRequest = aj.createXMLHttpRequest();
	aj.showLoading = function()
	{
		if(aj.waitId && (aj.XMLHttpRequest.readyState != 4 || aj.XMLHttpRequest.status != 200))
		{
			aj.waitId.style.display = '';
			aj.waitId.innerHTML = '<span><img src="' + imgpath + 'default/loading.gif" class="vm"> ' + aj.loading + '</span>';
		}
	};

	aj.processHandle = function() {
		if(aj.XMLHttpRequest.readyState == 4 && aj.XMLHttpRequest.status == 200)
		{
			if(aj.waitId && typeof waitId == 'object')
			{
				aj.waitId.style.display = 'none';
			}
			
			if(aj.recvType == 'HTML')
			{
				aj.resultHandle(aj.XMLHttpRequest.responseText, aj);
			}
			else if(aj.recvType == 'XML')
			{
				if(!aj.XMLHttpRequest.responseXML || !aj.XMLHttpRequest.responseXML.lastChild || aj.XMLHttpRequest.responseXML.lastChild.localName == 'parsererror')
				{
					aj.resultHandle('<a href="' + aj.targetUrl + '" target="_blank" style="color:red">内部错误，无法显示此内容</a>' , aj);
				}
				else
				{
					aj.resultHandle(aj.XMLHttpRequest.responseXML.lastChild.firstChild.nodeValue, aj);
				}
			}
			else if(aj.recvType == 'JSON')
			{
				var s = null;
				try
				{
					s = (new Function("return ("+aj.XMLHttpRequest.responseText+")"))();
				} 
				catch (e)
				{
					s = null;
				}
				aj.resultHandle(s, aj);
			}
		}
	};

	aj.get = function(targetUrl, resultHandle)
	{
		targetUrl = hostconvert(targetUrl);
		setTimeout(function(){aj.showLoading()}, 250);
		aj.targetUrl = targetUrl;
		aj.XMLHttpRequest.onreadystatechange = aj.processHandle;
		aj.resultHandle = resultHandle;
		if(window.XMLHttpRequest)
		{
			aj.XMLHttpRequest.open('GET', aj.targetUrl);
			aj.XMLHttpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
			aj.XMLHttpRequest.send(null);
		}
		else
		{
			aj.XMLHttpRequest.open("GET", targetUrl, true);
			aj.XMLHttpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
			aj.XMLHttpRequest.send();
		}
	};
	aj.post = function(targetUrl, sendString, resultHandle)
	{
		targetUrl = hostconvert(targetUrl);
		setTimeout(function(){aj.showLoading()}, 250);
		aj.targetUrl = targetUrl;
		aj.sendString = sendString;
		aj.XMLHttpRequest.onreadystatechange = aj.processHandle;
		aj.resultHandle = resultHandle;
		aj.XMLHttpRequest.open('POST', targetUrl);
		aj.XMLHttpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		aj.XMLHttpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
		aj.XMLHttpRequest.send(aj.sendString);
	};
	aj.getJSON = function(targetUrl, resultHandle)
	{
		aj.setRecvType('JSON');
		aj.get(targetUrl+'&ajaxdata=json', resultHandle);
	};
	aj.getHTML = function(targetUrl, resultHandle)
	{
		aj.setRecvType('HTML');
		aj.get(targetUrl+'&ajaxdata=html', resultHandle);
	};
	return aj;
}

//获取服务器信息显�?
function getHost(url) {
	var host = "null";
	if(typeof url == "undefined"|| null == url)
	{
		url = window.location.href;
	}
	var regex = /^\w+\:\/\/([^\/]*).*/;
	var match = url.match(regex);
	if(typeof match != "undefined" && null != match)
	{
		host = match[1];
	}
	return host;
}

function hostconvert(url)
{
	if(!url.match(/^https?:\/\//)) url = site_url + url;
	var url_host = getHost(url);
	var cur_host = getHost().toLowerCase();
	if(url_host && cur_host != url_host)
	{
		url = url.replace(url_host, cur_host); 
	}
	return url;
}

function getJsUrl(str)
{ 
	var pos,para,parastr;  
	var array =[] 
	//str = location.href;  
	parastr = str.split("?")[1];  
	var arr = parastr.split("&"); 
	for (var i=0;i<arr.length;i++)
	{ 
		array[arr[i].split("=")[0]]=arr[i].split("=")[1]; 
	} 
	return array; 
}

function newfunction(func) {
	var args = [];
	for(var i=1; i<arguments.length; i++) args.push(arguments[i]);
	return function(event) {
		doane(event);
		window[func].apply(window, args);
		return false;
	}
}

function evalscript(s)
{
	if(s.indexOf('<script') == -1) return s;
	var p = /<script[^\>]*?>([^\x00]*?)<\/script>/ig;
	var arr = [];
	while(arr = p.exec(s)) {
		var p1 = /<script[^\>]*?src=\"([^\>]*?)\"[^\>]*?(reload=\"1\")?(?:charset=\"([\w\-]+?)\")?><\/script>/i;
		var arr1 = [];
		arr1 = p1.exec(arr[0]);
		if(arr1)
		{
			appendscript(arr1[1], '', arr1[2], arr1[3]);
		}
		else
		{
			p1 = /<script(.*?)>([^\x00]+?)<\/script>/i;
			arr1 = p1.exec(arr[0]);
			appendscript('', arr1[2], arr1[1].indexOf('reload=') != -1);
		}
	}
	return s;
}

var evalscripts = [];


function $F(func, args, script)
{
	var run = function ()
	{
		var argc = args.length, s = '';
		for(i = 0;i < argc;i++)
		{
			s += ',args[' + i + ']';
		}
		eval('var check = typeof ' + func + ' == \'function\'');
		if(check)
		{
			eval(func + '(' + s.substr(1) + ')');
		}
		else
		{
			setTimeout(function () { checkrun(); }, 50);
		}
	};	
	var checkrun = function ()
	{
		if(JSLOADED[src])
		{
			
			run();
		}
		else
		{
			setTimeout(function () { checkrun(); }, 50);
		}
	};
	script = script || 'common_uicms';	
	src = site_url + imgpath + 'js/' + script + '.js';		
	if(!JSLOADED[src])
	{
		appendscript(src);
	}	
	checkrun();
}

// 跳转后得到cookie
// appendscript(arr1[1], '', arr1[2], arr1[3]);
function appendscript(src, text, reload, charset)
{
	var id = hash(src + text);	
	if(!reload && in_array(id, evalscripts)) return;
	if(reload && ui(id)) {
		ui(id).parentNode.removeChild(ui(id));
	}

	evalscripts.push(id);
	var scriptNode = document.createElement("script");
	scriptNode.type = "text/javascript";
	scriptNode.id = id;
	scriptNode.charset = charset ? charset : (BROWSER.firefox ? document.characterSet : document.charset);	
	try {
		if(src)
		{
			scriptNode.src = src;
			scriptNode.onloadDone = false;
			scriptNode.onload = function () {
				scriptNode.onloadDone = true;
				JSLOADED[src] = 1;
			};
			scriptNode.onreadystatechange = function () {
				if((scriptNode.readyState == 'loaded' || scriptNode.readyState == 'complete') && !scriptNode.onloadDone)
				{
					scriptNode.onloadDone = true;
					JSLOADED[src] = 1;
				}
			};
		}
		else if(text)
		{
			scriptNode.text = text;
		}
		document.getElementsByTagName('head')[0].appendChild(scriptNode);
	} catch(e) {}
}

function stripscript(s) {
	return s.replace(/<script.*?>.*?<\/script>/ig, '');
}

function ajaxupdateevents(obj, tagName) {
	tagName = tagName ? tagName : 'A';
	var objs = obj.getElementsByTagName(tagName);
	for(k in objs) {
		var o = objs[k];
		ajaxupdateevent(o);
	}
}

function ajaxupdateevent(o) {
	if(typeof o == 'object' && o.getAttribute) {
		if(o.getAttribute('ajaxtarget')) {
			if(!o.id) o.id = Math.random();
			var ajaxevent = o.getAttribute('ajaxevent') ? o.getAttribute('ajaxevent') : 'click';
			var ajaxurl = o.getAttribute('ajaxurl') ? o.getAttribute('ajaxurl') : o.href;
			_attachEvent(o, ajaxevent, newfunction('ajaxget', ajaxurl, o.getAttribute('ajaxtarget'), o.getAttribute('ajaxwaitid'), o.getAttribute('ajaxloading'), o.getAttribute('ajaxdisplay')));
			if(o.getAttribute('ajaxfunc')) {
				o.getAttribute('ajaxfunc').match(/(\w+)\((.+?)\)/);
				_attachEvent(o, ajaxevent, newfunction(RegExp.$1, RegExp.$2));
			}
		}
	}
}

function ajaxget(url, showid, waitid, loading, display, recall,recvType)
{	
	
	waitid = typeof waitid == 'undefined' || waitid === null ? showid : waitid;
	var x = new Ajax();	
	x.recvType = recvType ? recvType : 'XML';
	x.setLoading(loading);
	x.setWaitId(waitid);
	x.display = typeof display == 'undefined' || display == null ? '' : display;
	x.showId = ui(showid);

	if(url.substr(strlen(url) - 1) == '#')
	{
		url = url.substr(0, strlen(url) - 1);
		x.autogoto = 1;
	}	
	var url = url + '&inajax=1&ajaxtarget=' + showid;		
	x.get(url, function(s, x)
	{
		var evaled = false;
		if(s.indexOf('ajaxerror') != -1)
		{
			evalscript(s);
			evaled = true;
		}
		if(!evaled && (typeof ajaxerror == 'undefined' || !ajaxerror))
		{
			if(x.showId)
			{
				x.showId.style.display = x.display;
				ajaxinnerhtml(x.showId, s);				
				//ajaxupdateevents(x.showId);				
				if(x.autogoto) scroll(0, x.showId.offsetTop);
			}
		}
		ajaxerror = null;		
		if(recall && typeof recall == 'function')
		{
			recall();
		}
		else if(recall)
		{
			eval(recall);
		}
		if(!evaled) evalscript(s);
	});
}

// 登陆点击提交按钮之后
// ajaxpost('lsform', 'return_ls', 'return_ls','','1');
function ajaxpost(formid, showid, waitid, showidclass, submitbtn, recall)
{
	var waitid = typeof waitid == 'undefined' || waitid === null ? showid : (waitid !== '' ? waitid : '');
	var showidclass = !showidclass ? '' : showidclass;
	var ajaxframeid = 'ajaxframe';
	var ajaxframe  = ui(ajaxframeid);
	var formtarget = ui(formid).target;
	
	var handleResult = function()
	{
		var s = '';
		var evaled = false;		
		showloading('none');
		try {
			s = ui(ajaxframeid).contentWindow.document.XMLDocument.text;
		} catch(e) {
			try {
				s = ui(ajaxframeid).contentWindow.document.documentElement.firstChild.wholeText;
			} catch(e) {
				try {
					s = ui(ajaxframeid).contentWindow.document.documentElement.firstChild.nodeValue;
				} catch(e) {
					s = '内部错误，无法显示此内容';
				}
			}
		}
			
		if(s != '' && s.indexOf('ajaxerror') != -1)
		{
			evalscript(s);
			evaled = true;
		}		
		if(showidclass)
		{
			if(showidclass != 'onerror')
			{
				ui(showid).className = showidclass;
			}
			else
			{
				showError(s);
				ajaxerror = true;
			}
		}
		
		if(submitbtn)
		{
			submitbtn.disabled = false;
		}
		
		if(!evaled && (typeof ajaxerror == 'undefined' || !ajaxerror))
		{
			ajaxinnerhtml(ui(showid), s);
		}
		ajaxerror = null;
		if(ui(formid)) ui(formid).target = formtarget;
		if(typeof recall == 'function')
		{
			recall();
		}
		else
		{
			eval(recall);
		}
		if(!evaled) evalscript(s);
		ajaxframe.loading = 0;
		ui('append_parent').removeChild(ajaxframe.parentNode);
	};
	
	if(!ajaxframe)
	{
		var div = document.createElement('div');
		div.style.display = 'none';
		div.innerHTML = '<iframe name="' + ajaxframeid + '" id="' + ajaxframeid + '" loading="1"></iframe>';
		ui('append_parent').appendChild(div);
		ajaxframe = ui(ajaxframeid);
	}
	else if(ajaxframe.loading)
	{
		return false;
	}	
	_attachEvent(ajaxframe, 'load', handleResult);
	showloading();
	ui(formid).target = ajaxframeid;
	
	var action = ui(formid).getAttribute('action');
	
	if( isUndefined(action) || action == null)
	{
		var action = window.location.href	
	}
		
	action = hostconvert(action);	
	ui(formid).action = action.replace(/\&inajax\=1/g, '') + ( action.indexOf('?') != -1 ? '&' : '?' ) + 'inajax=1' + ( action.indexOf('handlekey=') != -1 ? '' : '&handlekey=' + formid);
	ui(formid).submit();
	if(submitbtn)
	{
		submitbtn.disabled = true;
	}
	doane();
	return false;
}

function hash(string, length) {
	var length = length ? length : 32;
	var start = 0;
	var i = 0;
	var result = '';
	filllen = length - string.length % length;
	for(i = 0; i < filllen; i++){
		string += "0";
	}
	while(start < string.length) {
		result = stringxor(result, string.substr(start, length));
		start += length;
	}
	return result;
}

//随机字符
function stringxor(s1, s2) {
	var s = '';
	var hash = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	var max = Math.max(s1.length, s2.length);
	for(var i=0; i<max; i++) {
		var k = s1.charCodeAt(i) ^ s2.charCodeAt(i);
		s += hash.charAt(k % 52);
	}
	return s;
}

function showPreview(val, id) {
	var showObj = ui(id);
	if(showObj) {
		showObj.innerHTML = val.replace(/\n/ig, "<bupdateseccoder />");
	}
}

function showloading(display, waiting)
{
	var display = display ? display : 'block';
	var waiting = waiting ? waiting : '请稍�?...';
	ui('ajaxwaitid').innerHTML = waiting;
	ui('ajaxwaitid').style.display = display;
}

function ajaxinnerhtml(showid, s)
{
	if(showid.tagName != 'TBODY')
	{
		showid.innerHTML = s;
	}
	else
	{
		while(showid.firstChild) {
			showid.firstChild.parentNode.removeChild(showid.firstChild);
		}
		var div1 = document.createElement('DIV');
		div1.id = showid.id+'_div';
		div1.innerHTML = '<table><tbody id="'+showid.id+'_tbody">'+s+'</tbody></table>';
		ui('append_parent').appendChild(div1);
		var trs = div1.getElementsByTagName('TR');
		var l = trs.length;
		for(var i=0; i<l; i++) {
			showid.appendChild(trs[0]);
		}
		var inputs = div1.getElementsByTagName('INPUT');
		var l = inputs.length;
		for(var i=0; i<l; i++) {
			showid.appendChild(inputs[0]);
		}
		div1.parentNode.removeChild(div1);
	}
}

function doane(event, preventDefault, stopPropagation) {
	var preventDefault = isUndefined(preventDefault) ? 1 : preventDefault;
	var stopPropagation = isUndefined(stopPropagation) ? 1 : stopPropagation;
	e = event ? event : window.event;
	if(!e) {
		e = getEvent();
	}
	if(!e) {
		return null;
	}
	if(preventDefault) {
		if(e.preventDefault) {
			e.preventDefault();
		} else {
			e.returnValue = false;
		}
	}
	if(stopPropagation) {
		if(e.stopPropagation) {
			e.stopPropagation();
		} else {
			e.cancelBubble = true;
		}
	}
	return e;
}


function showMenu(v)
{
	var ctrlid = isUndefined(v['ctrlid']) ? v : v['ctrlid'];
	var showid = isUndefined(v['showid']) ? ctrlid : v['showid'];
	var menuid = isUndefined(v['menuid']) ? showid + '_menu' : v['menuid'];
	var ctrlObj = ui(ctrlid);
	var menuObj = ui(menuid);
	if(!menuObj) return;
	var mtype = isUndefined(v['mtype']) ? 'menu' : v['mtype'];
	var evt = isUndefined(v['evt']) ? 'mouseover' : v['evt'];
	var pos = isUndefined(v['pos']) ? '43' : v['pos'];
	var layer = isUndefined(v['layer']) ? 1 : v['layer'];
	var duration = isUndefined(v['duration']) ? 2 : v['duration'];
	var timeout = isUndefined(v['timeout']) ? 250 : v['timeout'];
	var maxh = isUndefined(v['maxh']) ? 600 : v['maxh'];
	var cache = isUndefined(v['cache']) ? 1 : v['cache'];
	var drag = isUndefined(v['drag']) ? '' : v['drag'];
	var dragobj = drag && ui(drag) ? ui(drag) : menuObj;
	var fade = isUndefined(v['fade']) ? 0 : v['fade'];
	var cover = isUndefined(v['cover']) ? 0 : v['cover'];
	var zindex = isUndefined(v['zindex']) ? JSMENU['zIndex']['menu'] : v['zindex'];
	var ctrlclass = isUndefined(v['ctrlclass']) ? '' : v['ctrlclass'];
	var winhandlekey = isUndefined(v['win']) ? '' : v['win'];
	zindex = cover ? zindex + 500 : zindex;
	if(typeof JSMENU['active'][layer] == 'undefined')
	{
		JSMENU['active'][layer] = [];
	}

	for(i in EXTRAFUNC['showmenu']) {
		try {
			eval(EXTRAFUNC['showmenu'][i] + '()');
		} catch(e) {}
	}

	if(evt == 'click' && in_array(menuid, JSMENU['active'][layer]) && mtype != 'win')
	{
		hideMenu(menuid, mtype);
		return;
	}
	if(mtype == 'menu')
	{
		hideMenu(layer, mtype);
	}

	if(ctrlObj)
	{
		if(!ctrlObj.getAttribute('initialized'))
		{
			ctrlObj.setAttribute('initialized', true);
			ctrlObj.unselectable = true;

			ctrlObj.outfunc = typeof ctrlObj.onmouseout == 'function' ? ctrlObj.onmouseout : null;
			ctrlObj.onmouseout = function() {
				if(this.outfunc) this.outfunc();
				if(duration < 3 && !JSMENU['timer'][menuid]) {
					JSMENU['timer'][menuid] = setTimeout(function () {
						hideMenu(menuid, mtype);
					}, timeout);
				}
			};

			ctrlObj.overfunc = typeof ctrlObj.onmouseover == 'function' ? ctrlObj.onmouseover : null;
			ctrlObj.onmouseover = function(e) {
				doane(e);
				if(this.overfunc) this.overfunc();
				if(evt == 'click')
				{
					clearTimeout(JSMENU['timer'][menuid]);
					JSMENU['timer'][menuid] = null;
				}
				else
				{
					for(var i in JSMENU['timer'])
					{
						if(JSMENU['timer'][i])
						{
							clearTimeout(JSMENU['timer'][i]);
							JSMENU['timer'][i] = null;
						}
					}
				}
			};
		}
	}

	if(!menuObj.getAttribute('initialized'))
	{
		menuObj.setAttribute('initialized', true);
		menuObj.ctrlkey = ctrlid;
		menuObj.mtype = mtype;
		menuObj.layer = layer;
		menuObj.cover = cover;
		if(ctrlObj && ctrlObj.getAttribute('fwin')) {menuObj.scrolly = true;}
		menuObj.style.position = 'absolute';
		menuObj.style.zIndex = zindex + layer;
		menuObj.onclick = function(e) {
			return doane(e, 0, 1);
		};
		if(duration < 3)
		{
			if(duration > 1)
			{
				menuObj.onmouseover = function()
				{
					clearTimeout(JSMENU['timer'][menuid]);
					JSMENU['timer'][menuid] = null;
				};
			}
			if(duration != 1)
			{
				menuObj.onmouseout = function()
				{
					JSMENU['timer'][menuid] = setTimeout(function ()
					{
						hideMenu(menuid, mtype);
					}, timeout);
				};
			}
		}
		
		
		if(cover)
		{
			if( ui(menuid + '_cover') )
			{
				
			}
			else
			{
				var coverObj = document.createElement('div');
				coverObj.id = menuid + '_cover';			
				coverObj.style.position = 'absolute';
				coverObj.style.zIndex = menuObj.style.zIndex - 1;
				coverObj.style.left = coverObj.style.top = '0px';
				coverObj.style.width = '100%';
				coverObj.style.height = Math.max(document.documentElement.clientHeight, document.body.offsetHeight) + 'px';
				coverObj.style.backgroundColor = '#000';
				coverObj.style.filter = 'progid:DXImageTransform.Microsoft.Alpha(opacity=50)';
				coverObj.style.opacity = 0.5;
				coverObj.onclick = function () { hideMenu(); };
				ui('append_parent').appendChild(coverObj);
				_attachEvent(window, 'load', function () {
					coverObj.style.height = Math.max(document.documentElement.clientHeight, document.body.offsetHeight) + 'px';
				}, document);
			}
		}
	}
	if(drag)
	{
		dragobj.style.cursor = 'move';
		dragobj.onmousedown = function(event) {try{dragMenu(menuObj, event, 1);}catch(e){}};
	}
	if(cover) ui(menuid + '_cover').style.display = '';
	
	if(fade) {
		var O = 0;
		var fadeIn = function(O) {
			if(O > 100) {
				clearTimeout(fadeInTimer);
				return;
			}
			menuObj.style.filter = 'progid:DXImageTransform.Microsoft.Alpha(opacity=' + O + ')';
			menuObj.style.opacity = O / 100;
			O += 20;
			var fadeInTimer = setTimeout(function () {
				fadeIn(O);
			}, 40);
		};
		fadeIn(O);
		menuObj.fade = true;
	} else {
		menuObj.fade = false;
	}
	menuObj.style.display = '';
	if(ctrlObj && ctrlclass)
	{
		ctrlObj.className += ' ' + ctrlclass;
		menuObj.setAttribute('ctrlid', ctrlid);
		menuObj.setAttribute('ctrlclass', ctrlclass);
	}
	
	if(pos != '*') {
		setMenuPosition(showid, menuid, pos);
	}
	if(BROWSER.ie && BROWSER.ie < 7 && winhandlekey && ui('fwin_' + winhandlekey)) {
		ui(menuid).style.left = (parseInt(ui(menuid).style.left) - parseInt(ui('fwin_' + winhandlekey).style.left)) + 'px';
		ui(menuid).style.top = (parseInt(ui(menuid).style.top) - parseInt(ui('fwin_' + winhandlekey).style.top)) + 'px';
	}
	if(maxh && menuObj.scrollHeight > maxh) {
		menuObj.style.height = maxh + 'px';
		if(BROWSER.opera) {
			menuObj.style.overflow = 'auto';
		} else {
			menuObj.style.overflowY = 'auto';
		}
	}

	if(!duration) {
		setTimeout('hideMenu(\'' + menuid + '\', \'' + mtype + '\')', timeout);
	}

	if(!in_array(menuid, JSMENU['active'][layer])) JSMENU['active'][layer].push(menuid);
	menuObj.cache = cache;
	if(layer > JSMENU['layer'])
	{
		JSMENU['layer'] = layer;
	}
}
var delayShowST = null;



var dragMenuDisabled = false;
function dragMenu(menuObj, e, op) {
	e = e ? e : window.event;
	if(op == 1) {
		if(dragMenuDisabled || in_array(e.target ? e.target.tagName : e.srcElement.tagName, ['TEXTAREA', 'INPUT', 'BUTTON', 'SELECT'])) {
			return;
		}
		JSMENU['drag'] = [e.clientX, e.clientY];
		JSMENU['drag'][2] = parseInt(menuObj.style.left);
		JSMENU['drag'][3] = parseInt(menuObj.style.top);
		document.onmousemove = function(e) {try{dragMenu(menuObj, e, 2);}catch(err){}};
		document.onmouseup = function(e) {try{dragMenu(menuObj, e, 3);}catch(err){}};
		doane(e);
	}else if(op == 2 && JSMENU['drag'][0]) {
		var menudragnow = [e.clientX, e.clientY];
		menuObj.style.left = (JSMENU['drag'][2] + menudragnow[0] - JSMENU['drag'][0]) + 'px';
		menuObj.style.top = (JSMENU['drag'][3] + menudragnow[1] - JSMENU['drag'][1]) + 'px';
		menuObj.removeAttribute('top_');menuObj.removeAttribute('left_');
		doane(e);
	}else if(op == 3) {
		JSMENU['drag'] = [];
		document.onmousemove = null;
		document.onmouseup = null;
	}
}

function setMenuPosition(showid, menuid, pos)
{
	var showObj = ui(showid);
	var menuObj = menuid ? ui(menuid) : ui(showid + '_menu');
	if(isUndefined(pos) || !pos) pos = '43';
	var basePoint = parseInt(pos.substr(0, 1));
	var direction = parseInt(pos.substr(1, 1));
	var important = pos.indexOf('!') != -1 ? 1 : 0;
	var sxy = 0, sx = 0, sy = 0, sw = 0, sh = 0, ml = 0, mt = 0, mw = 0, mcw = 0, mh = 0, mch = 0, bpl = 0, bpt = 0;

	if(!menuObj || (basePoint > 0 && !showObj)) return;
	if(showObj) {
		sxy = fetchOffset(showObj);
		sx = sxy['left'];
		sy = sxy['top'];
		sw = showObj.offsetWidth;
		sh = showObj.offsetHeight;
	}
	mw = menuObj.offsetWidth;
	mcw = menuObj.clientWidth;
	mh = menuObj.offsetHeight;
	mch = menuObj.clientHeight;

	switch(basePoint) {
		case 1:
			bpl = sx;
			bpt = sy;
			break;
		case 2:
			bpl = sx + sw;
			bpt = sy;
			break;
		case 3:
			bpl = sx + sw;
			bpt = sy + sh;
			break;
		case 4:
			bpl = sx;
			bpt = sy + sh;
			break;
	}
	switch(direction) {
		case 0:
			menuObj.style.left = (document.body.clientWidth - menuObj.clientWidth) / 2 + 'px';
			mt = (document.documentElement.clientHeight - menuObj.clientHeight) / 2;
			break;
		case 1:
			ml = bpl - mw;
			mt = bpt - mh;
			break;
		case 2:
			ml = bpl;
			mt = bpt - mh;
			break;
		case 3:
			ml = bpl;
			mt = bpt;
			break;
		case 4:
			ml = bpl - mw;
			mt = bpt;
			break;
	}
	var scrollTop = Math.max(document.documentElement.scrollTop, document.body.scrollTop);
	var scrollLeft = Math.max(document.documentElement.scrollLeft, document.body.scrollLeft);
	if(!important) {
		if(in_array(direction, [1, 4]) && ml < 0) {
			ml = bpl;
			if(in_array(basePoint, [1, 4])) ml += sw;
		} else if(ml + mw > scrollLeft + document.body.clientWidth && sx >= mw) {
			ml = bpl - mw;
			if(in_array(basePoint, [2, 3])) {
				ml -= sw;
			} else if(basePoint == 4) {
				ml += sw;
			}
		}
		if(in_array(direction, [1, 2]) && mt < 0) {
			mt = bpt;
			if(in_array(basePoint, [1, 2])) mt += sh;
		} else if(mt + mh > scrollTop + document.documentElement.clientHeight && sy >= mh) {
			mt = bpt - mh;
			if(in_array(basePoint, [3, 4])) mt -= sh;
		}
	}
	if(pos.substr(0, 3) == '210') {
		ml += 69 - sw / 2;
		mt -= 5;
		if(showObj.tagName == 'TEXTAREA') {
			ml -= sw / 2;
			mt += sh / 2;
		}
	}
	if(direction == 0 || menuObj.scrolly) {
		if(BROWSER.ie && BROWSER.ie < 7) {
			if(direction == 0) mt += scrollTop;
		} else {
			if(menuObj.scrolly) mt -= scrollTop;
			menuObj.style.position = 'fixed';
		}
	}
	if(ml) menuObj.style.left = ml + 'px';
	if(mt) menuObj.style.top = mt + 'px';
	if(direction == 0 && BROWSER.ie && !document.documentElement.clientHeight) {
		menuObj.style.position = 'absolute';
		menuObj.style.top = (document.body.clientHeight - menuObj.clientHeight) / 2 + 'px';
	}
	if(menuObj.style.clip && !BROWSER.opera) {
		menuObj.style.clip = 'rect(auto, auto, auto, auto)';
	}
}

function hideMenu(attr, mtype)
{
	attr = isUndefined(attr) ? '' : attr;
	mtype = isUndefined(mtype) ? 'menu' : mtype;
	if(attr == '')
	{
		for(var i = 1; i <= JSMENU['layer']; i++)
		{
			hideMenu(i, mtype);
		}
		return;
	}
	else if(typeof attr == 'number')
	{
		for(var j in JSMENU['active'][attr])
		{
			hideMenu(JSMENU['active'][attr][j], mtype);
		}
		return;
	}
	else if(typeof attr == 'string')
	{
		var menuObj = ui(attr);
		if(!menuObj || (mtype && menuObj.mtype != mtype)) return;
		var ctrlObj = '', ctrlclass = '';
		if((ctrlObj = ui(menuObj.getAttribute('ctrlid'))) && (ctrlclass = menuObj.getAttribute('ctrlclass')))
		{
			var reg = new RegExp(' ' + ctrlclass);
			ctrlObj.className = ctrlObj.className.replace(reg, '');
		}
		clearTimeout(JSMENU['timer'][attr]);
		var hide = function()
		{
			if(menuObj.cache)
			{
				if(menuObj.style.visibility != 'hidden')
				{					
					menuObj.style.display = 'none';	
					if(menuObj.cover) ui(attr + '_cover').style.display = 'none';	
					/*二次制作*/			
					//menuObj.parentNode.removeChild(menuObj);
					//if(menuObj.cover) ui(attr + '_cover').parentNode.removeChild(ui(attr + '_cover'));
				}
			}
			else
			{
				menuObj.parentNode.removeChild(menuObj);
				if(menuObj.cover) ui(attr + '_cover').parentNode.removeChild(ui(attr + '_cover'));
			}
			var tmp = [];
			for(var k in JSMENU['active'][menuObj.layer])
			{
				if(attr != JSMENU['active'][menuObj.layer][k]) tmp.push(JSMENU['active'][menuObj.layer][k]);
			}
			JSMENU['active'][menuObj.layer] = tmp;
		};
		if(menuObj.fade) {
			var O = 100;
			var fadeOut = function(O) {
				if(O == 0) {
					clearTimeout(fadeOutTimer);
					hide();
					return;
				}
				menuObj.style.filter = 'progid:DXImageTransform.Microsoft.Alpha(opacity=' + O + ')';
				menuObj.style.opacity = O / 100;
				O -= 20;
				var fadeOutTimer = setTimeout(function () {
					fadeOut(O);
				}, 40);
			};
			fadeOut(O);
		} else {
			hide();
		}
	}
}

function getCurrentStyle(obj, cssproperty, csspropertyNS)
{
	if(obj.style[cssproperty])
	{
		return obj.style[cssproperty];
	}
	if (obj.currentStyle)
	{
		return obj.currentStyle[cssproperty];
	}
	else if (document.defaultView.getComputedStyle(obj, null))
	{
		var currentStyle = document.defaultView.getComputedStyle(obj, null);
		var value = currentStyle.getPropertyValue(csspropertyNS);
		if(!value)
		{
			value = currentStyle[cssproperty];
		}
		return value;
	}
	else if (window.getComputedStyle)
	{
		var currentStyle = window.getComputedStyle(obj, "");
		return currentStyle.getPropertyValue(csspropertyNS);
	}
}

function fetchOffset(obj, mode) {
	var left_offset = 0, top_offset = 0, mode = !mode ? 0 : mode;

	if(obj.getBoundingClientRect && !mode) {
		var rect = obj.getBoundingClientRect();
		var scrollTop = Math.max(document.documentElement.scrollTop, document.body.scrollTop);
		var scrollLeft = Math.max(document.documentElement.scrollLeft, document.body.scrollLeft);
		if(document.documentElement.dir == 'rtl') {
			scrollLeft = scrollLeft + document.documentElement.clientWidth - document.documentElement.scrollWidth;
		}
		left_offset = rect.left + scrollLeft - document.documentElement.clientLeft;
		top_offset = rect.top + scrollTop - document.documentElement.clientTop;
	}
	if(left_offset <= 0 || top_offset <= 0) {
		left_offset = obj.offsetLeft;
		top_offset = obj.offsetTop;
		while((obj = obj.offsetParent) != null)
		{
			position = getCurrentStyle(obj, 'position', 'position');
			if(position == 'relative')
			{
				continue;
			}
			left_offset += obj.offsetLeft;
			top_offset += obj.offsetTop;
		}
	}
	return {'left' : left_offset, 'top' : top_offset};
}

var showDialogST = null;

//显示对话�?
/*
	msg	提示内容
	mode	错误类型
	t 标题
	func 确定功能�?
	cover	锁屏
	funccancel 关闭后功能表
	leftmsg 页脚提示
	confirmtxt 确定按钮
	canceltxt 取消按钮
	closetime 关闭时间
	locationtime 跳转时间
*/

// 登陆成功后
// ('欢迎您回来，pp13438845536，现在将转入登录前页面', 'right', null, function () { window.location.href ='http://www.gter.net/offer/index'; }, 0, null, null, null, null, 3, 3)
function showDialog(msg, mode, t, func, cover, funccancel, leftmsg, confirmtxt, canceltxt, closetime, locationtime)
{
	clearTimeout(showDialogST);
	cover = isUndefined(cover) ? (mode == 'info' ? 0 : 1) : cover;
	leftmsg = isUndefined(leftmsg) ? '' : leftmsg;
	mode = in_array(mode, ['confirm', 'notice', 'info', 'right']) ? mode : 'alert';
	var menuid = 'fwin_dialog';
	var menuObj = ui(menuid);
	var showconfirm = 1;
	confirmtxtdefault = '确定';
	closetime = isUndefined(closetime) ? '' : closetime;
	closefunc = function () {
		if(typeof func == 'function') func();
		else eval(func);
		hideMenu(menuid, 'dialog');
	};
	if(closetime)
	{
		leftmsg = closetime + ' 秒后窗口关闭';
		showDialogST = setTimeout(closefunc, closetime * 1000);
		showconfirm = 0;
	}

	locationtime = isUndefined(locationtime) ? '' : locationtime;
	if(locationtime)
	{
		leftmsg = locationtime + ' 秒后页面跳转';
		showDialogST = setTimeout(closefunc, locationtime * 1000);
		showconfirm = 0;
	}
	confirmtxt = confirmtxt ? confirmtxt : confirmtxtdefault;
	canceltxt = canceltxt ? canceltxt : '取消';

	if(menuObj) hideMenu('fwin_dialog', 'dialog');
	menuObj = document.createElement('div');
	menuObj.style.display = 'none';
	menuObj.className = 'fwinmask';
	menuObj.id = menuid;
	ui('append_parent').appendChild(menuObj);
	var hidedom = '';
	if(!BROWSER.ie)
	{
		hidedom = '<style type="text/css">object{visibility:hidden;}</style>';
	}
	if(t=='none')
	{
		var s = hidedom + '<table cellpadding="0" cellspacing="0" class="fwin"><tr><td class="t_l"></td><td class="t_c"></td><td class="t_r"></td></tr><tr><td class="m_l"></td><td class="m_c">';
	}	
	else
	{
		var s = hidedom + '<table cellpadding="0" cellspacing="0" class="fwin"><tr><td class="t_l"></td><td class="t_c"></td><td class="t_r"></td></tr><tr><td class="m_l"></td><td class="m_c"><h3 class="flb"><em>';
		s += t ? t : '提示信息';
		s += '</em><span><a href="javascript:;" id="fwin_dialog_close" class="flbc" onclick="hideMenu(\'' + menuid + '\', \'dialog\')" title="关闭">关闭</a></span></h3>';
	}
	
	
	if(mode == 'info')
	{
		s += msg ? msg : '';
	}
	else
	{
		s += '<div class="c altw"><div class="' + (mode == 'alert' ? 'alert_error' : (mode == 'right' ? 'alert_right' : 'alert_info')) + '"><p>' + msg + '</p></div></div>';
		s += '<p class="o pns">' + (leftmsg ? '<span class="z xg1">' + leftmsg + '</span>' : '') + (showconfirm ? '<button id="fwin_dialog_submit" value="true" class="pn pnc"><strong>'+confirmtxt+'</strong></button>' : '');
		s += mode == 'confirm' ? '<button id="fwin_dialog_cancel" value="true" class="pn" onclick="hideMenu(\'' + menuid + '\', \'dialog\')"><strong>'+canceltxt+'</strong></button>' : '';
		s += '</p>';
	}
	s += '</td><td class="m_r"></td></tr><tr><td class="b_l"></td><td class="b_c"></td><td class="b_r"></td></tr></table>';
	menuObj.innerHTML = s;
	if(ui('fwin_dialog_submit')) ui('fwin_dialog_submit').onclick = function()
	{
		if(typeof func == 'function') func();
		else eval(func);
		hideMenu(menuid, 'dialog');
	};
	if(ui('fwin_dialog_cancel')) {
		ui('fwin_dialog_cancel').onclick = function() {
			if(typeof funccancel == 'function') funccancel();
			else eval(funccancel);
			hideMenu(menuid, 'dialog');
		};
		ui('fwin_dialog_close').onclick = ui('fwin_dialog_cancel').onclick;
	}
	showMenu({'mtype':'dialog','menuid':menuid,'duration':3,'pos':'00','zindex':JSMENU['zIndex']['dialog'],'cache':0,'cover':cover});
	try {
		if(ui('fwin_dialog_submit')) ui('fwin_dialog_submit').focus();
	} catch(e) {}
}


//显示窗口
// URL=http://www.gter.net/index.php?m=user&c=login&api=uicms&infloat=yes&handlekey=login&t=1429427975603&inajax=1&ajaxtarget=fwin_content_login
// showWindow('login', 'index.php?m=user&c=login&api=uicms', 'get',-1);	
function showWindow(k, url, mode, cache, menuv, cover)
{
	mode = isUndefined(mode) ? 'get' : mode;
	cache = isUndefined(cache) ? 0 : cache;
	cover = isUndefined(cover) ? 0 : true;
	var menuid = 'fwin_' + k;
	var menuObj = ui(menuid);
	var drag = null;
	var loadingst = null;
	var hidedom = '';
	if(disallowfloat && disallowfloat.indexOf(k) != -1)
	{
		if(BROWSER.ie) url += (url.indexOf('?') != -1 ?  '&' : '?') + 'referer=' + escape(location.href);
		location.href = url;
		doane();
		return;
	}

	var fetchContent = function()
	{
		if(mode == 'get')
		{
			menuObj.url = url;
			url += (url.search(/\?/) > 0 ? '&' : '?') + 'infloat=yes&handlekey=' + k;
			url += cache == -1 ? '&t='+(+ new Date()) : '';	
			ajaxget(url, 'fwin_content_' + k, null, '', '', function() {initMenu();show();});
		}
		else if(mode == 'post')
		{			
			menuObj.act = ui(url).action;
			ajaxpost(url, 'fwin_content_' + k, '', '', '', function() {initMenu();show();});
		}
		if(parseInt(BROWSER.ie) != 6)
		{
			loadingst = setTimeout(function() {showDialog('', 'info', '<img src="' + site_url + imgpath + 'default/loading.gif"> 请稍�?...')}, 500);
		}
	};
	var initMenu = function()
	{
		clearTimeout(loadingst);
		var objs = menuObj.getElementsByTagName('*');
		var fctrlidinit = false;
		for(var i = 0; i < objs.length; i++)
		{
			if(objs[i].id)
			{
				objs[i].setAttribute('fwin', k);
			}
			if(objs[i].className == 'flb' && !fctrlidinit)
			{
				if(!objs[i].id) objs[i].id = 'fctrl_' + k;
				drag = objs[i].id;
				fctrlidinit = true;
			}
		}
	};
	
	var show = function()
	{
		hideMenu('fwin_dialog', 'dialog');
		v = {'mtype':'win','menuid':menuid,'duration':3,'pos':'00','zindex':JSMENU['zIndex']['win'],'drag':typeof drag == null ? '' : drag,'cache':cache,'cover':cover};
		for(k in menuv)
		{
			v[k] = menuv[k];
		}		
		showMenu(v);
	};

	if(!menuObj)
	{
		menuObj = document.createElement('div');
		menuObj.id = menuid;
		menuObj.className = 'fwinmask';
		menuObj.style.display = 'none';
		ui('append_parent').appendChild(menuObj);
		evt = ' style="cursor:move" onmousedown="dragMenu(ui(\'' + menuid + '\'), event, 1)" ondblclick="hideWindow(\'' + k + '\')"';
		if(!BROWSER.ie) {
			hidedom = '<style type="text/css">object{visibility:hidden;}</style>';
		}
		menuObj.innerHTML = hidedom + '<table cellpadding="0" cellspacing="0" class="fwin"><tr><td class="t_l"></td><td class="t_c"' + evt + '></td><td class="t_r"></td></tr><tr><td class="m_l"' + evt + ')"></td><td class="m_c" id="fwin_content_' + k + '">'
			+ '</td><td class="m_r"' + evt + '"></td></tr><tr><td class="b_l"></td><td class="b_c"' + evt + '></td><td class="b_r"></td></tr></table>';
		if(mode == 'html')
		{
			ui('fwin_content_' + k).innerHTML = url;
			initMenu();
			show();
		}
		else
		{
			fetchContent();
		}
	}
	else if((mode == 'get' && (url != menuObj.url || cache != 1)) || (mode == 'post' && ui(url).action != menuObj.act))
	{
		fetchContent();
	}
	else
	{
		show();
	}
	doane();
}

//错误信息
function showError(msg, mode)
{
	
	var modes = mode ? mode : 'alert';
	var p = /<script[^\>]*?>([^\x00]*?)<\/script>/ig;
	msg = msg.replace(p, '');
	if(msg !== '')
	{
		showDialog(msg, modes, '提示信息', null, null, null, '', '', '', 3);
	}
}
//关闭弹窗
function hideWindow(k, all, clear) {
	all = isUndefined(all) ? 1 : all;
	clear = isUndefined(clear) ? 1 : clear;
	hideMenu('fwin_' + k, 'win');
	
	if(clear && ui('fwin_' + k))
	{
		ui('append_parent').removeChild(ui('fwin_' + k));
	}
	if(all)
	{
		hideMenu();
	}
}





var zoomstatus = 1;
//显示图片
function zoom(obj, zimg, nocover, pn, showexif)
{
	$F('_zoom', arguments);
}
//即时提示
function showPrompt(ctrlid, evt, msg, timeout)
{
	$F('_showPrompt', arguments);
}
//复制
function setCopy(text, msg)
{
	$F('_setCopy', arguments);
}
//复制ID内的代码
function copycode(obj)
{
	$F('_copycode', arguments);
}
//TAB切换
function switchTab(prefix, current, total, activeclass)
{
	$F('_switchTab', arguments);
}

//鼠标经过提示
function showTip(ctrlobj)
{
	$F('_showTip', arguments);
}
//颜色切换
function showColorBox(ctrlid, layer, k, bgcolor)
{
	$F('_showColorBox', arguments);
}
//表情
function smilies_show(id, smcols, seditorkey)
{
	$F('_smilies_show', arguments, 'smilies');
}

//单个附件上传
function uploadWindow(recall, type, module)
{
	$F('_upload_show', arguments, 'upload_one');
}


//幻灯�?
function slide(slide)
{
	$F('_slide', arguments, 'myfocus-2.0.1.full');
}

function initTab(frameId, type)
{
	$F('_initTab', arguments);
}

//ctrl+enter 
function ctrlEnter(event, btnId, onlyEnter)
{
	if(isUndefined(onlyEnter)) onlyEnter = 0;
	if((event.ctrlKey || onlyEnter) && event.keyCode == 13)
	{
		ui(btnId).click();
		return false;
	}
	return true;
}

//输入字数检�? 
function strLenCalc(obj, checklen, maxlen)
{
	var v = obj.value, charlen = 0, maxlen = !maxlen ? 200 : maxlen, curlen = maxlen, len = strlen(v);
	for(var i = 0; i < v.length; i++)
	{
		if(v.charCodeAt(i) < 0 || v.charCodeAt(i) > 255)
		{
			curlen -= charset == 'utf-8' ? 2 : 1;
		}
	}
	if(curlen >= len)
	{
		ui(checklen).innerHTML = curlen - len;
	}
	else
	{
		obj.value = mb_cutstr(v, maxlen, 0);
	}
}

function mb_cutstr(str, maxlen, dot) {
	var len = 0;
	var ret = '';
	var dot = !dot ? '...' : dot;
	maxlen = maxlen - dot.length;
	for(var i = 0; i < str.length; i++)
	{
		len += str.charCodeAt(i) < 0 || str.charCodeAt(i) > 255 ? (charset == 'utf-8' ? 3 : 2) : 1;
		if(len > maxlen)
		{
			ret += dot;
			break;
		}
		ret += str.substr(i, 1);
	}
	return ret;
}


//补丁通知
function patchNotice()
{
	if(ui('patch_notice'))
	{
		ajaxget('index.php?m=index&c=ajax&a=notice', 'patch_notice', '');
	}
}


//添加收藏�?
function addFavorite(url, title) {
	try {
		window.external.addFavorite(url, title);
	} catch (e){
		try {
			window.sidebar.addPanel(title, url, '');
        	} catch (e) {
			showDialog("请按 Ctrl+D 键添加到收藏�?", 'notice');
		}
	}
}
//设为主页
function setHomepage(sURL) {
	if(BROWSER.ie){
		document.body.style.behavior = 'url(#default#homepage)';
		document.body.setHomePage(sURL);
	} else {
		showDialog("�? IE 浏览器请手动将本站设为首�?", 'notice');
		doane();
	}
}

//点击改变长度
function rateStarHover(target,level)
{
	if(level ==  0)
	{
		ui(target).style.width = '';
	}
	else
	{
		ui(target).style.width = level * 16 + 'px';
	}
}

function parseurl(str, mode, parsecode)
{
	if(isUndefined(parsecode)) parsecode = true;
	if(parsecode) str= str.replace(/\s*\[code\]([\s\S]+?)\[\/code\]\s*/ig, function($1, $2) {return codetag($2);});
	str = str.replace(/([^>=\]"'\/@]|^)((((https?|ftp|gopher|news|telnet|rtsp|mms|callto|bctp|ed2k|thunder|qqdl|synacast):\/\/))([\w\-]+\.)*[:\.@\-\w\u4e00-\u9fa5]+\.([\.a-zA-Z0-9]+|\u4E2D\u56FD|\u7F51\u7EDC|\u516C\u53F8)((\?|\/|:)+[\w\.\/=\?%\-&;~`@':+!#]*)*)/ig, mode == 'html' ? '$1<a href="$2" target="_blank">$2</a>' : '$1[url]$2[/url]');
	str = str.replace(/([^\w>=\]"'\/@]|^)((www\.)([\w\-]+\.)*[:\.@\-\w\u4e00-\u9fa5]+\.([\.a-zA-Z0-9]+|\u4E2D\u56FD|\u7F51\u7EDC|\u516C\u53F8)((\?|\/|:)+[\w\.\/=\?%\-&;~`@':+!#]*)*)/ig, mode == 'html' ? '$1<a href="$2" target="_blank">$2</a>' : '$1[url]$2[/url]');
	str = str.replace(/([^\w->=\]:"'\.\/]|^)(([\-\.\w]+@[\.\-\w]+(\.\w+)+))/ig, mode == 'html' ? '$1<a href="mailto:$2">$2</a>' : '$1[email]$2[/email]');
	if(parsecode) {
		for(var i = 0; i <= DISCUZCODE['num']; i++) {
			str = str.replace("[\tDISCUZ_CODE_" + i + "\t]", DISCUZCODE['html'][i]);
		}
	}
	return str;
}
function codetag(text) {
	DISCUZCODE['num']++;
	if(typeof wysiwyg != 'undefined' && wysiwyg) text = text.replace(/<br[^\>]*>/ig, '\n');
	DISCUZCODE['html'][DISCUZCODE['num']] = '[code]' + text + '[/code]';
	return '[\tDISCUZ_CODE_' + DISCUZCODE['num'] + '\t]';
}




function AC_FL_RunContent()
{
	var str = '';
	var ret = AC_GetArgs(arguments, "clsid:d27cdb6e-ae6d-11cf-96b8-444553540000", "application/x-shockwave-flash");
	if(BROWSER.ie && !BROWSER.opera)
	{
		str += '<object ';
		for (var i in ret.objAttrs)
		{
			str += i + '="' + ret.objAttrs[i] + '" ';
		}
		str += '>';
		for (var i in ret.params)
		{
			str += '<param name="' + i + '" value="' + ret.params[i] + '" /> ';
		}
		str += '</object>';
	}
	else
	{
		str += '<embed ';
		for (var i in ret.embedAttrs)
		{
			str += i + '="' + ret.embedAttrs[i] + '" ';
		}
		str += '></embed>';
	}
	return str;
}

function AC_GetArgs(args, classid, mimeType)
{
	var ret = new Object();
	ret.embedAttrs = new Object();
	ret.params = new Object();
	ret.objAttrs = new Object();
	for (var i = 0; i < args.length; i = i + 2)
	{
		var currArg = args[i].toLowerCase();
		switch (currArg)
		{
			case "classid":break;
			case "pluginspage":ret.embedAttrs[args[i]] = 'http://www.macromedia.com/go/getflashplayer';break;
			case "src":ret.embedAttrs[args[i]] = args[i+1];ret.params["movie"] = args[i+1];break;
			case "codebase":ret.objAttrs[args[i]] = 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0';break;
			case "onafterupdate":case "onbeforeupdate":case "onblur":case "oncellchange":case "onclick":case "ondblclick":case "ondrag":case "ondragend":
			case "ondragenter":case "ondragleave":case "ondragover":case "ondrop":case "onfinish":case "onfocus":case "onhelp":case "onmousedown":
			case "onmouseup":case "onmouseover":case "onmousemove":case "onmouseout":case "onkeypress":case "onkeydown":case "onkeyup":case "onload":
			case "onlosecapture":case "onpropertychange":case "onreadystatechange":case "onrowsdelete":case "onrowenter":case "onrowexit":case "onrowsinserted":case "onstart":
			case "onscroll":case "onbeforeeditfocus":case "onactivate":case "onbeforedeactivate":case "ondeactivate":case "type":
			case "id":ret.objAttrs[args[i]] = args[i+1];break;
			case "width":case "height":case "align":case "vspace": case "hspace":case "class":case "title":case "accesskey":case "name":
			case "tabindex":ret.embedAttrs[args[i]] = ret.objAttrs[args[i]] = args[i+1];break;
			default:ret.embedAttrs[args[i]] = ret.params[args[i]] = args[i+1];
		}
	}
	ret.objAttrs["classid"] = classid;
	if(mimeType)
	{
		ret.embedAttrs["type"] = mimeType;
	}
	return ret;
}

function loadcss(cssname)
{
	if(!CSSLOADED[cssname])
	{
		if(!ui('css_' + cssname))
		{
			css = document.createElement('link');
			css.id = 'css_' + cssname,
			css.type = 'text/css';
			css.rel = 'stylesheet';
			css.href = site_url+'image/default/' + cssname + '.css';
			var headNode = document.getElementsByTagName("head")[0];
			headNode.appendChild(css);
		}
		else
		{
			ui('css_' + cssname).href = site_url+'image/default/' + cssname + '.css';
		}
		CSSLOADED[cssname] = 1;
	}
}

function explode(inputstring, separators, includeEmpties)
{
 
	inputstring = new String(inputstring);
	separators = new String(separators);
	if(separators == "undefined")
	{
		separators = " :;";
	}
	fixedExplode = new Array(1);
	currentElement = "";
	count = 0;
	for(x=0; x < inputstring.length; x++)
	{
		str = inputstring.charAt(x);
		if(separators.indexOf(str) != -1)
		{
			if ( ( (includeEmpties <= 0) || (includeEmpties == false)) && (currentElement == ""))
			{
				
			}
			else
			{
				fixedExplode[count] = currentElement;
				count++;
				currentElement = "";
			}
		}
		else
		{
			currentElement += str;
		}
	}	
	if (( ! (includeEmpties <= 0) && (includeEmpties != false)) || (currentElement != ""))
	{
		fixedExplode[count] = currentElement;
	}
	return fixedExplode;
}

function showTopLink()
{
	var ft = ui('ft');
	if(ft)
	{
		var scrolltop = ui('scrolltop'),
			sidehelper = ui('sidehelper'),
			viewPortHeight = parseInt(document.documentElement.clientHeight),
			scrollHeight =-( (document.documentElement && document.documentElement.scrollTop) || document.body.scrollTop),
			basew = parseInt(ft.clientWidth),
			sw = sidehelper.clientWidth;
		if (basew < 1000)
		{
			var left = parseInt(fetchOffset(ft)['left']);
			left = left < sw ? left * 2 - sw : left;
			sidehelper.style.left = ( basew + left ) + 'px';
		}
		else
		{
			sidehelper.style.left = 'auto';
			sidehelper.style.right = '20px';
		}

		if (BROWSER.ie && BROWSER.ie < 7)
		{
			sidehelper.style.top = viewPortHeight - scrollHeight - 150 + 'px';
		}
		if (scrollHeight < -100)
		{
			scrolltop.style.visibility = 'visible';
		}
		else
		{
			scrolltop.style.visibility = 'hidden';
		}
	}
}


function threadbegindisplay(type, w, h, s)
{

	ui('begincloseid').onclick = function()
	{
		ui('threadbeginid').style.display = 'none';
	};
	var imgobj = ui('threadbeginid');
	imgobj.style.left = (document.body.clientWidth - w)/2 + 'px';
	//imgobj.style.top = (document.body.clientHeight - h)/2 + 'px';	
	imgobj.style.top = (Math.max(document.documentElement.clientHeight, document.body.offsetHeight) - h)/2 + 'px';	 
	if(type == 1)
	{
		autozoom(w, h, s);
	}
	else if(type == 2)
	{
		autofade(w, h, s);
	}
	else
	{
		setTimeout(function()
		{
			ui('threadbeginid').style.display = 'none';
		}, s);
	}
}


function autofade(w, h, s)
{
	this.imgobj = ui('threadbeginid');
	this.opacity = 0;
	this.fadein = function()
	{
		if(BROWSER.ie)
		{
			this.imgobj.filters.alpha.opacity = this.opacity;
		}
		else
		{
			this.imgobj.style.opacity = this.opacity/100;
		}
		if(this.opacity >= 100)
		{
			setTimeout(this.fadeout, s);
			return;
		}
		this.opacity++;
		setTimeout(this.fadein, 50);
	};
	this.fadeout = function()
	{
		if(BROWSER.ie)
		{
			this.imgobj.filters.alpha.opacity = this.opacity;
		}
		else
		{
			this.imgobj.style.opacity = this.opacity/100;
		}
		if(this.opacity <= 0)
		{
			this.imgobj.style.display = 'none';
			return;
		}
		this.opacity--;
		setTimeout(this.fadeout, 50);
	};
	this.fadein();
}

function autozoom(w, h, s)
{
	this.height = 0;
	this.imgobj = ui('threadbeginid');
	this.imgobj.style.overflow = 'hidden';
	this.imgobj.style.display = '';
	this.autozoomin = function()
	{
		this.height += 5;
		if(this.height >= h)
		{
			this.imgobj.style.height = h + 'px';
			setTimeout(this.autozoomout, s);
			return;
		}
		this.imgobj.style.height = this.height + 'px';
		setTimeout(this.autozoomin, 50);
	};
	this.autozoomout = function()
	{
		this.height -= 5;
		if(this.height <= 0)
		{
			this.imgobj.style.height = 0 + 'px';
			this.imgobj.style.display = 'none';
			return;
		}
		this.imgobj.style.height = this.height + 'px';
		setTimeout(this.autozoomout, 50);
	};
	this.autozoomin();
}

function seng_mail(aid)
{
	//执行操作
	appendscript(site_url+'index.php?m=index&c=ajax&a=mail_send' + (aid ? '&id='+aid : ''));		
	return false;
}


function resizepic(thispic,sizes,type)
{ 
	sizes = sizes ? sizes : 200;
	if(type=='h')
	{
		if(thispic.height>sizes) thispic.height=sizes;
	}
	else
	{
		if(thispic.width>sizes) thispic.width=sizes;
	}
	
}



function attachimggetsrc(img)
{
	return ui(img).getAttribute('zoomfile') ? ui(img).getAttribute('zoomfile') : ui(img).getAttribute('file');
}

function hasClass(elem, className)
{
	return elem.className && (" " + elem.className + " ").indexOf(" " + className + " ") != -1;
}


function mobileplayer()
{
	var platform = navigator.platform;
	var ua = navigator.userAgent;
	var ios = /iPhone|iPad|iPod/.test(platform) && ua.indexOf( "AppleWebKit" ) > -1;
	var andriod = ua.indexOf( "Android" ) > -1;
	if(ios || andriod)
	{
		return true;
	}
	else
	{
		return false;
	}
}

function sound(f)
{
	var data = '<div style="float:left;"><embed src="'+site_url+'image/swf/'+f+'.swf" quality="high" type="application/x-shockwave-flash" height="0" width="0" hidden="true"/></div>';	
	ui("sound").innerHTML = data;
}

function json(text)
{
	var match;
	if ((match = /\{[\s\S]*\}|\[[\s\S]*\]/.exec(text)))
	{
		text = match[0];
	}
	var cx = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
	cx.lastIndex = 0;
	if (cx.test(text))
	{
		text = text.replace(cx, function (a)
		{
			return '\\u' + ('0000' + a.charCodeAt(0).toString(16)).slice(-4);
		});
	}
	if (/^[\],:{}\s]*$/.
	test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, '@').
	replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').
	replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) {
		return eval('(' + text + ')');
	}
	throw 'JSON parse error';
}

//列表
function set_logo(aid, url, identifier, swf_id)
{
	
	var tag_id = upload['customSettings']['progressTarget'];		
	var eles = ui(tag_id).getElementsByTagName('i');				
	for (i = 0, L = eles.length; i < L; i++)
	{
		eles[i].className = '';
	}
	
	if(ui(identifier+'_aid'))
	{
		if(aid == ui(identifier+'_aid').value)
		{
			ui(identifier+'_aid').value = '';
		}
		else
		{	
			ui(identifier+'_aid').value = aid;		
			ui('logo_' + aid).className = 'is_logo';
		}
	}
}


//删除
function att_del(aid, identifier, swf_id)
{
	var swf = ui(swf_id);
	if(swf)
	{
		
		file_upload_limit = parseInt(upload.settings.file_upload_limit);
		file_queue_limit = parseInt(upload.settings.file_queue_limit);

		upload.setFileUploadLimit( file_upload_limit+1 );
		upload.setFileQueueLimit( file_queue_limit+1 );
		
		ui('list_img_'+aid).innerHTML = '';
		swf.className = "progressBarError";	
		swf.style.width = "";		
		swf.style.display = "none";
		swf.style.height = "0px";
		swf.style.opacity = "0";
		
		if(ui(identifier+'_aid') && ui(identifier+'_aid').value == aid)
		{
			if(ui(identifier+'_aid'))ui(identifier+'_aid').value = '';
			if(ui(identifier+'_url'))ui(identifier+'_url').value = '';
			if(ui(identifier+'_img'))ui(identifier+'_img').innerHTML = '';	
		}
		
		
	}
	else
	{
		if(ui(identifier+'_aid'))ui(identifier+'_aid').value = '';
		if(ui(identifier+'_url'))ui(identifier+'_url').value = '';
		if(ui(identifier+'_img'))ui(identifier+'_img').innerHTML = '';	
	}
		
	ATTACHORIMAGE = 0;
	//执行删除	
	ui_ajax('index.php?m=index&c=upload&a=delete','aid=' + aid);
}
