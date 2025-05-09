export default {
    title: 'AWS S3下载工具文档',
    description: '一个用于下载AWS S3文件夹的Python工具文档',
    themeConfig: {
        nav: [
            { text: '首页', link: '/' },
            { text: '指南', link: '/guide/' },
            { text: 'API参考', link: '/api/' }
        ],
        sidebar: [
            {
                text: '简介',
                items: [
                    { text: '什么是S3下载工具', link: '/introduction/what-is' },
                    { text: '快速开始', link: '/introduction/getting-started' }
                ]
            },
            {
                text: '使用指南',
                items: [
                    { text: '基本用法', link: '/guide/basic-usage' },
                    { text: '高级选项', link: '/guide/advanced-options' },
                    { text: '匿名访问', link: '/guide/anonymous-access' },
                    { text: '目录结构保留', link: '/guide/keep-structure' },
                    { text: '故障排除', link: '/guide/troubleshooting' }
                ]
            }
        ],
        socialLinks: [
            { icon: 'github', link: 'https://github.com/yourusername/s3-downloader' }
        ]
    }
}