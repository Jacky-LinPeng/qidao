# 栖岛公开网站

无需构建的 GitHub Pages 静态站点。发布目录为此目录，包含 `index.html`、`privacy.html`、`support.html`、`styles.css`、`assets/` 与 `.nojekyll`。不要将 App 源码或签名资料复制进公开网站仓库。

站点基址：`https://jacky-linpeng.github.io/qidao/`。所有站内路径均为相对路径，可作为项目站点部署。

本地验证：`python3 test_site.py`。本地预览：在此目录执行 `python3 -m http.server 8765`，再打开 `http://localhost:8765/`。

网站不依赖 JavaScript、CDN、外部字体或构建工具。图片为应用现有原创素材的 JPEG 压缩与尺寸优化副本。视觉组合为排版示意，已在页面中标注。

上线前需要将计划发布状态、设备支持范围与最终 App Store 信息核对。没有正式下载地址时保留“即将上线”，不要添加虚构链接。

当前本地发布稿为 235 张壁纸、9 分类；配套小组件仍为六套主题。发布前必须确认应用内容已全部生成，并通过包含九张精选的 `test_site.py` 引用检查。新增精选来自 `oriental-01`、`architecture-01`、`textures-01`，只做 JPEG 压缩和缩小，不放大，也不宣称 4K。
