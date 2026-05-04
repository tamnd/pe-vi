{% set rawUrl = 'https://raw.githubusercontent.com/tamnd/pe-vi/main/source/' + page.source %}
<div class="post-md-actions">
  <a href="{{ rawUrl }}" target="_blank" rel="noopener" class="post-md-btn">Xem markdown</a>
  <button class="post-md-btn" onclick="peviCopyMd('{{ rawUrl }}', this)">Sao chép markdown</button>
</div>
<script>
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
