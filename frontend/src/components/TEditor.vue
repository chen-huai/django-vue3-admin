<template>
  <div class="my-tinymce">
     <Editor v-model="contentValue" :init="myInit" :disabled="disabled"/>
  </div>
</template>

<script>
import {url} from '@/api/url'
import { onMounted,onUnmounted, reactive, toRefs, watch,nextTick } from 'vue'
import axios from 'axios'
// 引入tinymce编辑器
import Editor from '@tinymce/tinymce-vue'
import tinymce from 'tinymce/tinymce' // tinymce默认hidden，不引入则不显示编辑器
// 导入配置文件
import './teditorjs/importTinymce'
import { init } from './teditorjs/config'
import {setStorage,getStorage} from '@/utils/util'
let token = getStorage('logintoken')

export default {
  name: 'tEditor',
    components: {
    Editor
  },
  props: {
    // 绑定文本值
    modelValue: {
      type: String,
      default: ''
    },
    // placeholder
    placeholder: {
      type: String,
      default: '请输入内容'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    // 默认样式
    style: {
      type: Object,
      default: () => {
        return { width: '100%', heigth: '300' }
      }
    },
    // 图片上传服务器地址
    imgUploadUrl: {
      type: String,
      default: ''
    },
    // 是否隐藏
    hidden: {
      type: Boolean,
      default: false
    },
  },
  setup (props, { emit }) {
    const state = reactive({
      myInit: customer(init), // 初始化
      contentValue: props.modelValue, // 绑定文本
      timeout: null,
    })
    token = getStorage('logintoken')

    onMounted(() => {
      tinymce.init({})
      window.addEventListener("focusin", onFocusIn,true);
    })

    onUnmounted(()=>{
        // tinymce.remove()
        window.removeEventListener("focusin", onFocusIn);
    })

    // 侦听文本变化并传给外界
    watch(() => state.contentValue, (n) => {
      debounce(() => {
        emit('update:modelValue', state.contentValue)
      })
    })
    // 侦听默认值 外界第一次传进来一个 v-model 就赋值给 contentValue
    watch(() => props.modelValue, (n) => {
      if (n && n !== state.contentValue) {
        state.contentValue = n
      }
    })
    function  onFocusIn(e){
        e.stopImmediatePropagation()//阻止当前和后面的一系列事件
    }
    function debounce (fn, wait = 400)  {
      // console.log('进到了防抖', wait)
      if (state.timeout !== null) {
        clearTimeout(state.timeout)
      }
      state.timeout = setTimeout(fn, wait)
    }

    // 参数自定义初始化
    function customer (init) {
      // 允许外界传进来高度和placeholder
      init.height = props.style.heigth
      init.placeholder = props.placeholder

      // 粘贴图片 自动处理 base64
      init.urlconverter_callback = (url, node, onSave, name) => {
        if (node === 'img' && url.startsWith('blob:')) {
          tinymce.activeEditor && tinymce.activeEditor.uploadImages()
        }
        return url
      }
      // 图片上传
      init.images_upload_handler = (blobInfo, success, failure) => {
        imgUploadFn(blobInfo, success, failure)
      }
      return init
    }

    function imgUploadFn (blobInfo, success, failure) {
      // 可以限制图片大小
      // if (blobInfo.blob().size / 1024 / 1024 > 2) {
      //   failure('上传失败，图片大小请控制在 2M 以内')
      // } else {}
      const params = new FormData()
      params.append('file', blobInfo.blob())
      const config = {
        headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': 'JWT '+token,  // 可选参数(服务器上传验证需要) 如果需要token验证，假设你的token有存放在sessionStorage
        }
      }
      const uploadurl = url + 'platformsettings/uploadplatformimg/'
      // 图片上传
      axios.post(uploadurl, params, config).then(res => {
          console.log(res)
        if (res.data.code == 2000) {
            //这里很重要，你图片上传成功后，img的src需要在这里添加，res.path就是你服务器返回的图片链接。
              let imgpath=''
              if (res.data.data.data[0].indexOf("://")>=0){
                  imgpath = res.data.data.data[0]

              }else{
                  imgpath = url.split('/api')[0]+res.data.data.data[0]
              }
             success(imgpath) // 上传成功，在成功函数里填入图片路径
             // console.log('[文件上传]', res.data)
        } else {
          failure('上传失败')
        }
      }).catch(() => {
        failure('上传出错，服务器开小差了呢')
      })
    }

    return ({
      ...toRefs(state),
      customer,
      debounce
    })
  }
}
</script>

<style lang="css" >
    .my-tinymce{
        width: 100%;
    }
    .tox-notifications-container {
      display: none;
    }
    /*.tox-tinymce-aux {*/
    /*  z-index: 5000 !important;*/
    /*}*/
</style>