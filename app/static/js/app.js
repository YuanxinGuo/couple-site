// 全局 JS 工具

document.addEventListener('DOMContentLoaded', function() {
  // 图片加载错误处理
  document.querySelectorAll('img').forEach(function(img) {
    img.addEventListener('error', function() {
      this.style.display = 'none';
    });
  });
});

// 防抖函数
function debounce(fn, delay) {
  var timer;
  return function() {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function() { fn.apply(context, args); }, delay);
  };
}
