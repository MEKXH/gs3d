export default {
    title: 'G3SD文档',
    description: '通用AWS S3下载工具',
    head: [
        ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
        ['link', { rel: 'alternate icon', href: '/favicon.svg' }],
    ],
    // 如果部署到GitHub Pages子目录
    // base: '/G3SD/',
    themeConfig: {
        // 添加logo到导航栏
        logo: '/logo.svg',

        // 导航栏配置
        nav: [
            { text: '首页', link: '/' },
            { text: '指南', link: '/guide/' },
            { text: 'API参考', link: '/api/' }
        ],

        // 侧边栏配置
        sidebar: {
            '/guide/': [
                {
                    text: '指南',
                    items: [
                        { text: '指南首页', link: '/guide/' },
                        { text: '基本用法', link: '/guide/basic-usage' },
                        { text: '高级选项', link: '/guide/advanced-options' },
                        { text: '匿名访问', link: '/guide/anonymous-access' },
                        { text: '目录结构保留', link: '/guide/keep-structure' },
                        { text: '故障排除', link: '/guide/troubleshooting' }
                    ]
                }
            ],
            '/introduction/': [
                {
                    text: '介绍',
                    items: [
                        { text: '介绍首页', link: '/introduction/' },
                        { text: '什么是S3下载工具', link: '/introduction/what-is' },
                        { text: '快速开始', link: '/introduction/getting-started' }
                    ]
                }
            ],
            '/api/': [
                {
                    text: 'API参考',
                    items: [
                        { text: '命令行参数', link: '/api/' }
                    ]
                }
            ]
        },

        // 社交链接
        socialLinks: [
            { icon: 'github', link: 'https://github.com/yourusername/G3SD' }
        ],

        // 页脚配置
        footer: {
            message: '使用MIT许可证发布',
            copyright: 'Copyright © 2025'
        },

        // 搜索配置
        search: {
            provider: 'local'
        }
    }
}