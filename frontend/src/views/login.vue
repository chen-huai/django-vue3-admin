<template>
    <div class="lyouters">
      <canvas id="lyadmincanvas" @click.stop="handleAnimationState()"></canvas>
      <div class="login-config">
          <el-button :icon="siteThemeStore.siteTheme == 'dark'?'sunny':'moon'" circle type="info" @click="setSiteTheme"></el-button>
          <el-dropdown trigger="click" placement="bottom-end" @command="changeLang" style="margin-left: 10px">
              <el-button circle>
                  <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24" width="1.2em" height="1.2em" data-v-12008bb2=""><path fill="currentColor" d="m18.5 10l4.4 11h-2.155l-1.201-3h-4.09l-1.199 3h-2.154L16.5 10h2zM10 2v2h6v2h-1.968a18.222 18.222 0 0 1-3.62 6.301a14.864 14.864 0 0 0 2.336 1.707l-.751 1.878A17.015 17.015 0 0 1 9 13.725a16.676 16.676 0 0 1-6.201 3.548l-.536-1.929a14.7 14.7 0 0 0 5.327-3.042A18.078 18.078 0 0 1 4.767 8h2.24A16.032 16.032 0 0 0 9 10.877a16.165 16.165 0 0 0 2.91-4.876L2 6V4h6V2h2zm7.5 10.885L16.253 16h2.492L17.5 12.885z"></path></svg>
              </el-button>
              <template #dropdown>
                  <el-dropdown-menu>
                      <el-dropdown-item v-for="item in lang" :key="item.value" :command="item" :class="{'lydpselected':language==item.value}">{{item.name}}</el-dropdown-item>
                  </el-dropdown-menu>
              </template>
          </el-dropdown>
      </div>
      <div class="login-wrap box" :style="{'--animationState':animationState}">
        <el-form label-position="left" :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="demo-ruleForm login-container">
            <h3 class="title">
                <div class="login-logo">
                   <img style="width: 100%;" src="../assets/logo.png" alt="logo">
               </div>
<!--                <img style="height: 55px;margin-bottom: 10px" src="../assets/logo.png" alt="logo">-->
                <span>{{ $t('login.loginInTitle') }}</span>
            </h3>
          <el-form-item prop="username">
            <el-input type="text" size="large" style="font-size: 16px" v-model.trim="ruleForm.username" auto-complete="off" :placeholder="$t('login.loginAccount')" maxlength="60">
              <template #prepend>
                  <el-icon :size="20"><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" size="large" style="font-size: 16px" v-model.trim="ruleForm.password" auto-complete="off" :placeholder="$t('login.loginPWD')" maxlength="60">
                <template #prepend>
                  <el-icon :size="20"><lock /></el-icon>
                </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="captcha">
            <el-input type="text"  size="large" style="font-size: 16px" v-model.trim="ruleForm.captcha" auto-complete="off" @keyup.enter="submitForm('ruleForm')" :placeholder="$t('login.code')">
                 <template #prepend>
                    <el-icon :size="20"><circle-check /></el-icon>
                  </template>
                  <template #append>
                    <img class="login-code" :src="image_base" @click="getCaptcha"/>
                  </template>
            </el-input>
          </el-form-item>
          <el-checkbox class="remember" v-model="rememberpassword">{{$t('login.rememberMe')}}</el-checkbox>
          <el-form-item style="width:100%">
            <el-button type="primary" size="large" :loading="loadingLg" style="width:100%;font-size: 18px" @click="submitForm('ruleForm')">{{$t('login.login')}}</el-button>
          </el-form-item>
        </el-form>
      </div>
       <div class="login-copyright">
           Copyright © 2022 django-vue-lyadmin All rights reserved.
       </div>
    </div>
</template>
<script >
  import {login,apiSystemWebRouter,getCaptcha} from '@/api/api'
  import {systemTree} from "@/utils/menuTree.js"
  import {delCookie, getCookie, setCookie} from '@/utils/util'
  import {useMutitabsStore} from "@/store/mutitabs";
  import {useSiteThemeStore} from "@/store/siteTheme";
  import {setStorage,getStorage} from '@/utils/util'
  import i18n from '@/locales'


  export default {
    name: 'login',
    setup(){
        const mutitabsstore = useMutitabsStore()
        const siteThemeStore = useSiteThemeStore()
        const { t } = i18n.global
        return { mutitabsstore,siteThemeStore,t }

    },
    data() {
      return {
        loadingLg:false,
        logining: false,
        rememberpassword: false,
        ruleForm: {
            username: '',
            password: '',
            captcha:'',
            captchaKey: null,
        },
        loginFlag:false,
        rules: {
            username: [{required: true, message: this.t('login.AccountError'), trigger: 'blur'}],
            password: [{required: true, message: this.t('login.PWError'), trigger: 'blur'}],
            captcha: [{required: true, message: this.t('login.codeError'), trigger: 'blur'}],
        },
        image_base: null,
        allmenu:[],
        language:this.siteThemeStore.language,
        lang: [
            {
                name: '简体中文',
                value: 'zh-cn',
            },
            {
                name: 'English',
                value: 'en',
            }
        ],
        //动画
        animationState:'paused',
        WIDTH:"",
        HEIGHT:"",
        POINT :"",
        canvas:null,
        context:null,
        circleArr:[],
        beginX:null,
        beginY:null,
        closeX:null,
        closeY:null,
        moveX:null,
        moveY:null,
        x:null,
        y:null,
        r:null,
        o:null,
      }
    },
      mounted() {
        this.init();
        let that = this
		setInterval(function () {
			for (var i = 0; i < that.POINT; i++) {
				var cir = that.circleArr[i];
				cir.x += cir.moveX;
				cir.y += cir.moveY;
				if (cir.x > that.WIDTH) cir.x = 0;
				else if (cir.x < 0) cir.x = that.WIDTH;
				if (cir.y > that.HEIGHT) cir.y = 0;
				else if (cir.y < 0) cir.y = that.HEIGHT;
			}
			that.draw();
		}, 25);
        window.addEventListener('resize', this.listenResize);
      },
      unmounted() {
          // 页面销毁，去掉监听事件
          window.removeEventListener("resize", this.listenResize);
      },
      created() {
        //动态添加该页面meta viewport 手机适配
        if(document.querySelector("meta[name='viewport']")){
            document.querySelector("meta[name='viewport']")["content"] = "width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=no"
        }
        //请求数据
        this.getuserpassword()
        this.getCaptcha()
      },
      beforeRouteLeave(to, form, next){
          //离开页面去除动态添加该页面meta viewport 手机适配
          document.querySelector("meta[name='viewport']")["content"] = this.getCurrentWith()
          next()
      },
      methods: {
        //设置主题
        setSiteTheme(){
            if(this.siteThemeStore.siteTheme=='light'){
                this.siteThemeStore.setSiteTheme('dark')
            }else{
                this.siteThemeStore.setSiteTheme('light')
            }
        },
        //设置语言
        changeLang(command){
            this.language = command.value
            this.siteThemeStore.setLanguage(command.value)
        },
        handleAnimationState(){
          if(this.animationState === 'paused'){
            this.animationState = 'running'
          }else{
            this.animationState = 'paused'
          }
        },
        // 计算搜索栏的高度
        listenResize() {
            this.$nextTick(() => {
                this.init()
            })
        },
        //线条：开始xy坐标，结束xy坐标，线条透明度
         Line (x, y, _x, _y, o) {
            this.beginX = x,
            this.beginY = y,
            this.closeX = _x,
            this.closeY = _y,
            this.o = o;
            return {
                beginX :x,
                beginY :y,
                closeX:_x,
                closeY:_y,
                o :o
            }
        },
        //点：圆心xy坐标，半径，每帧移动xy的距离
         Circle (x, y, r, moveX, moveY) {
            this.x = x,
            this.y = y,
            this.r = r,
            this.moveX = moveX,
            this.moveY = moveY;
            return{
                x:x,
                y: y,
                r:r,
                moveX:moveX,
                moveY: moveY
            }
        },
        //生成max和min之间的随机数
        num (max, _min) {
            var min = arguments[1] || 0;
            return Math.floor(Math.random()*(max-min+1)+min);
        },
        // 绘制原点
         drawCricle (cxt, x, y, r, moveX, moveY) {
            var circle =this.Circle(x, y, r, moveX, moveY)
            cxt.beginPath()
            cxt.arc(circle.x, circle.y, circle.r, 0, 2*Math.PI)
            cxt.closePath()
            cxt.fill();
            return circle;
        },
        //绘制线条
        drawLine (cxt, x, y, _x, _y, o) {
            var line = this.Line(x, y, _x, _y, o)
            cxt.beginPath()
            cxt.strokeStyle = 'rgba(0,0,0,'+ o +')'
            cxt.moveTo(line.beginX, line.beginY)
            cxt.lineTo(line.closeX, line.closeY)
            cxt.closePath()
            cxt.stroke();

        },
        //初始化生成原点
        init () {
             //定义画布宽高和生成点的个数
            this.WIDTH = window.innerWidth
            this.HEIGHT = window.innerHeight
            this.POINT = 18;
            this.canvas = document.getElementById('lyadmincanvas');
            this.canvas.width = this.WIDTH-2,
            this.canvas.height = this.HEIGHT-2;
            this.context = this.canvas.getContext('2d');
            this.context.strokeStyle = 'rgba(0,0,0,0.06)',
            this.context.strokeWidth = 1,
            this.context.fillStyle = 'rgba(0,0,0,0.05)';
            this.circleArr = [];
            for (var i = 0; i < this.POINT; i++) {
                this.circleArr.push(this.drawCricle(this.context, this.num(this.WIDTH), this.num(this.HEIGHT), this.num(18, 5), this.num(20, -20)/40, this.num(20, -20)/40));
            }
            this.draw();
        },

	    //每帧绘制
         draw () {
            this.context.clearRect(0,0,this.canvas.width, this.canvas.height);
            for (var i = 0; i < this.POINT; i++) {
                this.drawCricle(this.context, this.circleArr[i].x, this.circleArr[i].y, this.circleArr[i].r);
            }
            for (var i = 0; i < this.POINT; i++) {
                for (var j = 0; j < this.POINT; j++) {
                    if (i + j < this.POINT) {
                        var A = Math.abs(this.circleArr[i+j].x - this.circleArr[i].x),
                            B = Math.abs(this.circleArr[i+j].y - this.circleArr[i].y);
                        var lineLength = Math.sqrt(A*A + B*B);
                        var C = 1/lineLength*7-0.009;
                        var lineOpacity = C > 0.03 ? 0.03 : C;
                        if (lineOpacity > 0) {
                            this.drawLine(this.context, this.circleArr[i].x, this.circleArr[i].y, this.circleArr[i+j].x, this.circleArr[i+j].y, lineOpacity);
                        }
                    }
                }
            }
        },
        getCurrentWith(){
            var designWidth = 375;
            var deviceWidth = parseInt(window.screen.width) || parseInt(document.documentElement.clientWidth);  //获取当前设备的屏幕宽度
            // var deviceScale = deviceWidth/designWidth;
            var deviceScale = 0.6;
            var ua = navigator.userAgent;
            //获取当前设备类型（安卓或苹果）

            if (ua && /Android (\d+.\d+)/.test(ua)) {
                // +",user-scalable=no"
                return "width=680,initial-scale="+deviceScale+",minimum-scale="+deviceScale+",maximum-scale="+deviceScale;
            }
            else if (ua && /iPhone|ipad|ipod|ios/.test(ua)){
                return "width=680,initial-scale="+deviceScale+",minimum-scale="+deviceScale+",maximum-scale="+deviceScale;
            }
            else {
                return '';
            }
        },
      // 获取用户名密码
      // 获取菜单
      getMenu() {
        this.menuTitle=''
        this.allmenu=[]
        this.loadingLg=true
        apiSystemWebRouter().then(res=>{
          if(res.code == 2000) {
            let menuTree = []
            if(res.data.data.length > 0) {
              let childrenList = res.data.data.filter(item=> item.parent && item.visible == 1)
              let parentList = res.data.data.filter(item=> !item.parent && item.visible == 1)
              if(parentList.length >0) {
                parentList.forEach(item=>{
                  let menuTreeChildren=[]
                  let children = childrenList.filter(itema=>itema.parent == item.id)
                  let children2 = childrenList.filter((item)=>{
                    return children.every((item1)=>{
                        return item.path != item1.path;
                    })
                  })
                  children.forEach(itemb=>{
                    let cmenuTreeChildren=[]
                    let cchildren = children2.filter(itemc=>itemc.parent == itemb.id)
                    cchildren.forEach(itemd=>{
                        cmenuTreeChildren.push(({
                          text:itemd.name,
                          id:itemd.id,
                          attributes:{
                            url:itemd.web_path,
                            icon:itemd.icon
                          },
                          hasChildren: false,
                          hasParent:true
                        }))
                    })
                    let chasChildren = false
                    if(cmenuTreeChildren.length>0){
                        chasChildren = true
                    }
                    menuTreeChildren.push(({
                      text:itemb.name,
                      id:itemb.id,
                      attributes:{
                        url:itemb.web_path,
                        icon:itemb.icon
                      },
                      children:cmenuTreeChildren,
                      hasChildren: chasChildren,
                      hasParent:true,
                    }))
                  })
                  menuTree.push({
                    text:item.name,
                    id:item.id,
                    attributes:{
                      url:children.length >0 ? children[0].web_path :item.web_path,
                      icon:item.icon
                    },
                    hasChildren: children.length >0,
                    hasParent:false,
                    children:menuTreeChildren,
                  })
                  item.children=[...children]
                })
              }

              // 操作权限管控
              let menuList=[]
              res.data.data.forEach(item=>{
                //console.log(item,'item---- 菜单权限---')
                menuList.push({
                  url:item.web_path,
                  moduleName:item.name,
                  menuPermission:item.menuPermission
                })
              })
              setStorage('menuList', JSON.stringify(menuList))
            }
            // console.log(menuTree,'menuTree-----')
            this.allmenu =  menuTree
            if(this.allmenu.length >0) {
              this.$nextTick(()=>{
                this.$router.replace({path: `/${this.allmenu[0].attributes.url}`})
              })
            } else {
               this.mutitabsstore.logout('false')
               this.$router.push({path: '/login'})
               sessionStorage.clear()
               localStorage.clear()
               this.loadingLg=false
               this.$message.warning('暂无授权任何菜单权限~')
            }

            setStorage('allmenu', JSON.stringify(this.allmenu))
            //优化首次登录第一个标签显示问题
            let tabsPage = ""
            let TabsValue = ""
            if(menuTree[0].hasChildren){
                tabsPage = [{"title":menuTree[0].children[0].text,"name":menuTree[0].children[0].attributes.url,"query":{}}]
                TabsValue = menuTree[0].children[0].attributes.url
            }else{
                tabsPage = [{"title":menuTree[0].text,"name":menuTree[0].attributes.url,"query":{}}]
                TabsValue = menuTree[0].attributes.url
            }
            this.mutitabsstore.firstTabs([tabsPage,TabsValue])
            this.$forceUpdate()
          } else {
            this.$message.warning(res.msg)
          }

          this.loadingLg=false
        })

        this.$forceUpdate()
      },


      getuserpassword() {
        if (getCookie('username') != '' && getCookie('password') != '') {
          this.ruleForm.username = getCookie('username')
          this.ruleForm.password = getCookie('password')
          this.rememberpassword = true
        }
      },

      /**
       * 获取验证码
       */
      getCaptcha () {
        getCaptcha().then((ret) => {
          this.ruleForm.captcha = null
          this.ruleForm.captchaKey = ret.data.data.key
          this.image_base = ret.data.data.image_base
        })
      },

      //获取info列表
      submitForm(formName) {

        this.$refs[formName].validate(valid => {
          if (valid) {
            this.loadingLg = true
            login(this.ruleForm).then(async res => {
              this.loadingLg = false
              if (res.code === 2000) {
                if (this.rememberpassword) {
                  //保存帐号到cookie，有效期7天
                  await setCookie('username', this.ruleForm.username, 7)
                  //保存密码到cookie，有效期7天
                  await setCookie('password', this.ruleForm.password, 7)
                } else {
                  await delCookie('username')
                  await delCookie('password')
                }
                this.mutitabsstore.setLogintoken(res.data.access)
                this.mutitabsstore.setUserName(res.data.name)
                this.mutitabsstore.setUserId(res.data.userId)
                this.mutitabsstore.setRefresh(res.data.refresh)
                this.getMenu()
              } else {
                this.getCaptcha()
                this.$message.error(res.msg)
                return false
              }
            })
          } else {
            this.$message.error('请输入用户名密码/验证码！')
            return false
          }
        })

      }
    }
  }
</script>

<style lang="scss" scoped>
    //django-vue-lyadmin css
    ::v-deep(.el-input__inner){
        &::placeholder{
            font-size: 14px !important;
        }
    }
    ::v-deep(.el-input-group__append){
        background-color: var(--el-bg-color)  !important;
        width: 70px;
    }
    ::v-deep(.el-input-group__prepend){
        background-color: var(--el-bg-color) !important;
        .el-icon{
            color: var(--el-color-primary);
        }
    }
   .lyouters{
        width: 100%;
        height: 100%;
   }
   .login-config{
       position: absolute;
       top:20px;
       right: 20px;
   }
   ::v-deep(.lydpselected){
        background-color: var(--el-dropdown-menuItem-hover-fill);
        color: var(--el-dropdown-menuItem-hover-color);
   }
   .login-logo{
        overflow: hidden;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        -webkit-box-shadow: 0 4px 40px rgb(0 0 0 / 7%);
        box-shadow: 0 4px 40px rgb(0 0 0 / 7%);
        background-color: var(--el-bg-color);
        z-index: 10;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
   }
   .login-copyright{
        color: #999;
        width: 100%;
        position: fixed;
        bottom: 30px;
       text-align: center;
   }
  .login-wrap {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    box-sizing: border-box;
    display: flex;
    align-items: center;
    .login-container {
      inset: 2px;
      z-index: 2;
      border-radius: 10px;
      margin: 0px auto;
      width: 374px;
      height: 469px;
      padding: 30px 35px 15px 35px;
      background: var(--el-bg-color);
      border: 1px solid #eaeaea;
      text-align: left;
      box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0.1);
    }
    .title {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        justify-content: center;
        font-size: 19px;
        margin: 0px auto 25px auto;
        color: var(--el-color-primary);
        font-weight: 700;
    }
    .remember {
      margin: 0px 0px 15px 0px;
    }
  }
  .market-login{
    width: 1200px;
    margin: 0 auto;
    display: flex;
    border-radius: 8px;
    background: var(--el-bg-color);
    box-shadow: 0px 0px 12px 0px rgba(0, 0, 0, 0.08);
    .login-container1{
      width: 510px;
      margin-left: 95px;
      .login-img{
        width: 500px;
      }
      .title{
        font-size: 48px;
        font-family: PingFangSC-Medium, PingFang SC;
        font-weight: 500;
        color: var(--el-color-primary);
        line-height: 67px;
        letter-spacing: 1px;
        margin: 60px auto 72px;
      }
      .el-form-item{
        margin-bottom: 72px;
        input{
          padding: 0;
          text-indent:0;
          margin-top: 20px;
        }
        .el-form-item__label{
          font-size: 20px;
          font-weight: 400;
          color: rgba(0, 0, 0, 0.56);
          line-height: 28px;
        }
      }
      .el-form-item.is-required:not(.is-no-asterisk)>.el-form-item__label:before{
        content:''
      }
      .el-input__inner{
        border: 0 !important;
        border-bottom: 2px solid rgba(0, 0, 0, 0.16) !important;
        border-radius: 0;
        font-size: 24px;
        font-weight: 500;
        color: rgba(0, 0, 0, 0.84);
      }
      .el-input{
        position: relative;
      }
      .el-input:after{
        position: absolute;
        content: '';
        width:0;
        height: 2px;
        left: 0;
        bottom: 3px;
        z-index: 2;
        transition: all 0.5s;
        background: #0072FF;
      }
      .el-input.hasTxt:after{
        width: 100%;
        .el-input__inner{
          border-right: 0 !important;
        }
      }
      .loadingLg{
        width:100%;
        height: 72px;
        background: #0072FF;
        box-shadow: 0px 5px 15px 0px rgba(0, 114, 255, 0.25);
        border-radius: 4px;
        font-size: 24px;
        font-family: PingFangSC-Medium, PingFang SC;
        font-weight: 500;
        color: var(--el-bg-color);
      }
    }
  }
  @media only screen and (max-width: 450px) {
     .box{
      width: 100% !important;
    }
  }
  @media screen and (max-width: 1600px) {
    .market-login{
      width: 1050px;
      .login-img {
        width: 350px;
      }

      .login-container1 {
        .el-form-item{
          margin-bottom: 50px;
        }
        .title {
          margin: 40px auto;
        }
      }
    }
  }
  .login-code {
      height: 40px - 2px;
      display: block;
      margin: 0px -20px;
      border-top-right-radius: 2px;
      border-bottom-right-radius: 2px;
    }
    .box {
        width: 450px;
        height: 520px;
        background: var(--el-bg-color);
        overflow: hidden;
        border-radius: 10px;
    }
    .box::before {
        content: '';
        z-index: 1;
        position: absolute;
        top: -50%;
        left: -50%;
        width: 450px;
        height: 520px;
        transform-origin: bottom right;
        background: linear-gradient(0deg, transparent, var(--el-color-primary), var(--el-color-primary));
        animation: animate 10s linear infinite var(--animationState);
        animation-play-state: var(--animationState);
        -webkit-animation-play-state:var(--animationState);
    }

    .box::after {
        content: '';
        z-index: 1;
        position: absolute;
        top: -50%;
        left: -50%;
        width: 450px;
        height: 520px;
        transform-origin: bottom right;
        background: linear-gradient(0deg, transparent, var(--el-color-primary), var(--el-color-primary));
        animation: animate 10s linear infinite var(--animationState);
        animation-delay: -5s;
        animation-play-state: var(--animationState);
        -webkit-animation-play-state:var(--animationState);
    }

    @keyframes animate {
        0% {
            transform: rotate(0deg);
        }

        100% {
            transform: rotate(360deg);
        }
    }
</style>