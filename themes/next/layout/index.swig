{% extends '_layout.swig' %}
{% import '_macro/sidebar.swig' as sidebar_template with context %}

{% block title %}{{ title }}{%- if theme.index_with_subtitle and subtitle %} - {{ subtitle }}{%- endif %}{% endblock %}

{% block class %}index posts-expand{% endblock %}

{% block content %}

<h2>Về Project Euler</h2>
<img src="images/avatar.png" alt="Leonhard Euler (1707-1783)" style="margin:10px;float:right;">
<h3>Project Euler là gì?</h3>
<p>Project Euler là một chuỗi bài toán toán học và lập trình máy tính đầy thử thách. Để giải được chúng, không chỉ cần kiến thức toán học: dù toán học giúp bạn tìm ra các phương pháp thanh lịch và hiệu quả, hầu hết bài toán vẫn cần đến máy tính và kỹ năng lập trình.<br><br>
Động lực khởi tạo Project Euler, và duy trì nó đến ngày nay, là tạo ra một nền tảng cho những tâm hồn tò mò được khám phá những lĩnh vực mới mẻ và học hỏi kiến thức trong bầu không khí vui vẻ, thú vị.
</p>
<br>
<h3>Những bài toán này dành cho ai?</h3>
<p>Đối tượng mà Project Euler hướng đến bao gồm học sinh cảm thấy chương trình học cơ bản chưa đủ thỏa mãn, người lớn không có nền tảng toán học chuyên sâu nhưng yêu thích toán, và những chuyên gia muốn rèn giũa thêm kỹ năng giải quyết vấn đề và tư duy toán học.</p>
<br>
<h3>Ai cũng có thể giải được không?</h3>
<p>Các bài toán có độ khó khác nhau, và với nhiều người, việc giải toán là một quá trình học tập liên hoàn. Nghĩa là, mỗi khi bạn giải xong một bài, bạn sẽ tiếp thu được một khái niệm mới giúp bạn tiếp cận những bài trước đây chưa thể làm được. Vì vậy, người tham gia kiên trì sẽ dần dần giải được tất cả các bài, dù chậm hay nhanh.
</p>
<br>
<h3>Bước tiếp theo?</h3>
<p>Để theo dõi tiến trình, bạn cần tạo tài khoản và bật Cookies. Nếu đã có tài khoản, hãy <a href="https://projecteuler.net/sign_in">đăng nhập</a>, còn chưa thì <a href="https://projecteuler.net/register">đăng ký</a> -- hoàn toàn miễn phí!</p>
<p>Vì các bài toán khá thử thách, bạn có thể muốn xem qua <a href="https://projecteuler.net/problems">danh sách bài toán</a> trước khi đăng ký.</p>
<blockquote class="blockquote-center"><em>"Project Euler tồn tại để khuyến khích, thử thách và phát triển kỹ năng cũng như niềm vui của bất kỳ ai có hứng thú với thế giới toán học kỳ diệu."</em>
</blockquote>

{% endblock %}

{% block sidebar %}
  {{ sidebar_template.render(false) }}
{% endblock %}
