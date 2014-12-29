one_kick_install_pptpd_on_ubuntu
================================

在ubuntu debian 上一键安装pptpd并自动配置。
执行：
<pre><code>
curl https://raw.githubusercontent.com/zhangtf/one_kick_install_pptpd_on_ubuntu/master/one_kick_install_pptpd.py | python
</code></pre>

执行完毕后编辑/etc/ppp/chap-secret文件在里面添加账户密码，格式如下
<pre><code>
  client        server  secret                  IP addresses
  用户名        pptpd   密码	                  *
</code></pre>
