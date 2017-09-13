/**
 * DevSummit Auth API client - dsa
 * designed to interact with auth Rest-API of Devsummit, using AJAX
 * will be used across all the web app (admin) interfaces
 * include this in any html template, after jquery script import
 * by @erdivartanovich
 */

(function (global) {
    
    const baseStorage = 'devsummitadmin';

    const ajaxObj = (url, methodType, payloads, onSuccess) => ({
        url : 'api/v1/'+url,
        type: methodType,
        data: JSON.stringify(payloads),
        contentType: "application/json; charset=utf-8",
        dataType   : "json",
        headers: {
            Authorization: dsa.acess_token()
        },
        success: onSuccess ? function(result){
            if(result['expired']) {
                clearCredential();
                window.location.href = '/login';
            } else {
                onSuccess(result);
            }
        } : null
    });

    const ajaxObjForm = (url, methodType, payloads, onSuccess) => ({
        url : 'api/v1/'+url,
        type: methodType,
        data: payloads,
        processData: false,
        dataType: 'json',
        contentType: false,
        headers: {
            'Authorization': dsa.acess_token()
        },
        success: onSuccess ? function(result){
            if(result['expired']) {
                clearCredential();
                window.location.href = '/login';
            } else {
                onSuccess(result);
            }
        } : null,
        error: function(err) {
            console.log(err)
        }
    });

    function storeCredential(data){
      Object.keys(data).map((key)=>{
        localStorage.setItem(baseStorage+'-'+key, data[key]);
      })
    }

    function clearCredential(){
        localStorage.removeItem(baseStorage+'-access_token');
        localStorage.removeItem(baseStorage+'-refresh_token');
    }

    var dsa = {}

    /* Request service To Api */
    dsa.get = function(url, onSuccess=null) {
        $.ajax(ajaxObj(url, 'GET', null, onSuccess));
    };

    dsa.post = function(url, payloads=null, onSuccess=null) {
        $.ajax(ajaxObj(url, 'POST', payloads, onSuccess));
    };

    dsa.patch = function(url, payloads=null, onSuccess=null) {
        $.ajax(ajaxObj(url, 'PUT', payloads, onSuccess));
    };

    dsa.delete = function(url, onSuccess=null) {
        $.ajax(ajaxObj(url, 'DELETE', {}, onSuccess));
    };

    dsa.acess_token = function() {
        const token = !!localStorage[baseStorage+'-access_token'] ? localStorage[baseStorage+'-access_token'] : '';
        return token;
    }
    dsa.refresh_token = function() {
        const refresh = !!localStorage[baseStorage+'-refresh_token'] ? localStorage[baseStorage+'-refresh_token'] : '';
        return refresh;
    }

    dsa.getForm = function(url, onSuccess=null) {
        $.ajax(ajaxObjForm(url, 'GET', null, onSuccess));
    };

    dsa.postForm = function(url, payloads=null, onSuccess=null) {
        $.ajax(ajaxObjForm(url, 'POST', payloads, onSuccess));
    };

    dsa.patchForm = function(url, payloads=null, onSuccess=null) {
        $.ajax(ajaxObjForm(url, 'PATCH', payloads, onSuccess));
    };
    
    dsa.request = function(url, method, payloads, onSuccess){
        $.ajax({
            url : url,
            type: method,
            data: JSON.stringify(payloads),
            contentType: "application/json; charset=utf-8",
            dataType   : "json",
            headers: {
            Authorization: dsa.acess_token()
            },
            success    : function(result){
                if(result['expired']) {
                    clearCredential();
                    window.location.href = '/login';
                } else {
                    onSuccess(result);
                }
            }
        });
    } 

    /* Login func */
    dsa.login = function(payloads, onSuccess) {
        $.ajax({
            url : "/auth/login",
            type: "POST",
            data: JSON.stringify(payloads),
            contentType: "application/json; charset=utf-8",
            dataType   : "json",
            success    : function(result){
                const success=result['meta']['success']
                if (success) {
                    var data = result['data']
                    //store token and refresh token
                    storeCredential(data);
                    //store user data
                    data = result['included'];
                    storeCredential(data);
                    window.location.href = "/";
                }
                onSuccess(success, result);
            }
        });
    };

    /* logout func */
    dsa.logout = function() {
        clearCredential();
        window.location.href = "/login";
    }

    /* isLogin func */
    dsa.isLogin = function() {
        return (!!dsa.acess_token())
    }

    /* get user data */
    dsa.getUser = function(source='storage') {
        var user = {};
        if (source='storage') {
            user.first_name = localStorage[baseStorage+'-first_name'];
            user.last_name = localStorage[baseStorage+'-last_name'];
            user.username = localStorage[baseStorage+'-username'];
            user.role_id = localStorage[baseStorage+'-role_id'];
            user.id = localStorage[baseStorage+'-id'];
            user.avatar = localStorage[baseStorage+'-url'];
            user.email = localStorage[baseStorage+'-email'];
            user.created_at = localStorage[baseStorage+'-created_at'];
        }
        return user;
    }

    // AMD support
    if (typeof define === 'function' && define.amd) {
        define(function () { return dsa; });
    // CommonJS and Node.js module support.
    } else if (typeof exports !== 'undefined') {
        // Support Node.js specific `module.exports` (which can be a function)
        if (typeof module !== 'undefined' && module.exports) {
            exports = module.exports = dsa;
        }
        // But always support CommonJS module 1.1.1 spec (`exports` cannot be a function)
        exports.dsa = dsa;
    } else {
        global.dsa = dsa;
    }
})(this);