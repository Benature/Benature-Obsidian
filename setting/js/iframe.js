class Iframe {
  youtube(dv, id, ratio = `9/16`) {
    dv.el(
      `div`,
      `<div style="display: block; position: relative; width: 100%; height: 0px; --aspect-ratio:${ratio}; padding-bottom: calc(var(--aspect-ratio) * 100%);"><iframe src="https://www.youtube.com/embed/${id}" allow="fullscreen" style="position: absolute; top: 0px; left: 0px; height: 100%; width: 100%;"></iframe></div>`
    );
  }
}
