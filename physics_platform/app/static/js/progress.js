/**
 * progress.js
 * 视频学习进度追踪模块
 * 功能：每 10 秒上报播放进度，页面关闭时使用 sendBeacon 上报最终状态
 */
(function() {
    'use strict';

    var TRACK_INTERVAL = 10000; // 10 秒上报一次
    var trackTimer = null;
    var videoId = null;
    var player = null;
    var hasReported = false;

    /**
     * 初始化进度追踪
     * @param {number} vId - 视频 ID
     * @param {object} vjsPlayer - Video.js 播放器实例
     */
    function init(vId, vjsPlayer) {
        videoId = vId;
        player = vjsPlayer;

        if (!videoId || !player) return;

        // 定时上报
        trackTimer = setInterval(reportProgress, TRACK_INTERVAL);

        // 页面离开时上报
        window.addEventListener('beforeunload', reportFinal);
        window.addEventListener('pagehide', reportFinal);

        // 视频播放结束时标记完成
        player.on('ended', function() {
            reportProgress(100);
        });
    }

    /**
     * 计算当前播放进度百分比
     * @returns {number} 0-100
     */
    function getProgress() {
        if (!player) return 0;
        var current = player.currentTime() || 0;
        var duration = player.duration() || 1;
        return Math.min(Math.round((current / duration) * 100), 100);
    }

    /**
     * 获取当前播放位置（秒）
     * @returns {number}
     */
    function getCurrentTime() {
        return player ? Math.round(player.currentTime() || 0) : 0;
    }

    /**
     * 上报进度（普通 fetch 方式）
     * @param {number} [overrideProgress] - 可选：强制覆盖进度值
     */
    function reportProgress(overrideProgress) {
        var progress = overrideProgress != null ? overrideProgress : getProgress();
        var data = {
            video_id: videoId,
            progress: progress,
            current_time: getCurrentTime(),
            timestamp: Date.now()
        };

        // 尝试 fetch 上报
        try {
            var csrfMeta = document.querySelector('meta[name="csrf-token"]');
            fetch('/api/progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfMeta ? csrfMeta.content : ''
                },
                body: JSON.stringify(data),
                keepalive: true
            }).catch(function() {
                // 静默失败，不打断用户
            });
        } catch (e) {
            // 静默失败
        }

        // 更新页面上的进度条
        updateProgressBar(progress);
    }

    /**
     * 页面卸载时用 sendBeacon 上报
     */
    function reportFinal() {
        if (hasReported) return;
        hasReported = true;

        if (trackTimer) {
            clearInterval(trackTimer);
            trackTimer = null;
        }

        var progress = getProgress();

        try {
            if (navigator.sendBeacon) {
                var formData = new FormData();
                formData.append('video_id', videoId);
                formData.append('progress', progress);
                formData.append('current_time', getCurrentTime());
                formData.append('timestamp', Date.now());
                formData.append('final', 'true');
                navigator.sendBeacon('/api/progress', formData);
            }
        } catch (e) {
            // 静默失败
        }
    }

    /**
     * 更新页面上所有相关进度条
     * @param {number} progress - 0-100
     */
    function updateProgressBar(progress) {
        var bars = document.querySelectorAll('#videoProgress');
        bars.forEach(function(bar) {
            bar.style.width = progress + '%';
            bar.setAttribute('aria-valuenow', progress);
        });
    }

    // =============================================
    // 公开 API
    // =============================================
    window.PhysicsProgress = {
        init: init,
        getProgress: getProgress,
        report: reportProgress
    };
})();
