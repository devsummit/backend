/**
 * DevSummit Auth API client
 * designed to interact with auth Rest-API of Devsummit, using AJAX
 * will be used across all the web app (admin) interfaces
 * 
 * by @erdivartanovich
 */

var script = document.createElement('script');

script.src = '//code.jquery.com/jquery-1.11.0.min.js';
document.getElementsByTagName('head')[0].appendChild(script); 

(function (global) {
    'use strict';
    
    const baseStorage = 'devsummitadmin';

    function storeCredential(data){
      Object.keys(data).map((key)=>{
        localStorage.setItem(baseStorage+'-'+key, data[key]);
      })
    }

    function clearCredential(){
        localStorage.removeItem(baseStorage+'-access_token');
        localStorage.removeItem(baseStorage+'-refresh_token');
    }

    var DevsummitAuth = {}

    DevsummitAuth.acess_token = function() {
        const token = !!localStorage[baseStorage+'-access_token'] ? localStorage[baseStorage+'-access_token'] : '';
        return token;
    }
    DevsummitAuth.refresh_token = function() {
        const refresh = !!localStorage[baseStorage+'-refresh_token'] ? localStorage[baseStorage+'-refresh_token'] : '';
        return refresh;
    }

    /* Login func */
    DevsummitAuth.login = function(payloads, onSuccess) {
        $.ajax({
            url : "/auth/login",
            type: "POST",
            data: JSON.stringify(payloads),
            contentType: "application/json; charset=utf-8",
            dataType   : "json",
            success    : function(result){
                const success=result['meta']['success']
                if (success) {
                    const credential_name = result['included']['username'];
                    const data = result['data']
                    storeCredential(data);
                }
                onSuccess(success);
            }
        });
    };

    /* logout func */
    DevsummitAuth.logout = function() {
        clearCredential();
        window.location.reload(true);
    }

    /* isLogin func */
    DevsummitAuth.isLogin = function() {
        return (!!DevsummitAuth.acess_token())
    }

    // set module alias
    window.DevsummitAuth = window.dsa = DevsummitAuth; 

    // AMD support
    if (typeof define === 'function' && define.amd) {
        define(function () { return DevsummitAuth; });
    // CommonJS and Node.js module support.
    } else if (typeof exports !== 'undefined') {
        // Support Node.js specific `module.exports` (which can be a function)
        if (typeof module !== 'undefined' && module.exports) {
            exports = module.exports = DevsummitAuth;
        }
        // But always support CommonJS module 1.1.1 spec (`exports` cannot be a function)
        exports.DevsummitAuth = DevsummitAuth;
    } else {
        global.DevsummitAuth = DevsummitAuth;
    }
})(this);