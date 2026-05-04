{% set rawUrl = 'https://raw.githubusercontent.com/tamnd/pe-vi/main/source/' + page.source %}
<div id="post-md-actions" class="post-md-actions">
  <a href="{{ rawUrl }}" target="_blank" rel="noopener" class="post-md-btn">Xem markdown</a>
  <button class="post-md-btn" onclick="peviCopyMd('{{ rawUrl }}', this)">Sao chép markdown</button>
</div>
<script>
(function() {
  var actions = document.getElementById('post-md-actions');
  var links = document.querySelectorAll('.post-body a[href*="projecteuler.net/problem="]');
  for (var i = 0; i < links.length; i++) {
    var p = links[i].closest('p');
    if (p) { p.parentNode.insertBefore(actions, p); break; }
  }
})();

function peviCopyMd(url, btn) {
  fetch(url)
    .then(function(r) { return r.text(); })
    .then(function(text) { return navigator.clipboard.writeText(text); })
    .then(function() {
      var orig = btn.textContent;
      btn.textContent = 'Đã sao chép!';
      setTimeout(function() { btn.textContent = orig; }, 1500);
    })
    .catch(function() {
      btn.textContent = 'Lỗi';
      setTimeout(function() { btn.textContent = 'Sao chép markdown'; }, 1500);
    });
}
</script>
