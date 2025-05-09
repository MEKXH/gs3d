import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
    ...DefaultTheme,
    enhanceApp({ app, router, siteData }) {
        // 这里可以添加自定义应用逻辑，如自定义组件或插件
    }
}