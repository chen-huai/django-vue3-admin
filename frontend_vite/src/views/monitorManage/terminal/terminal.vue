<template>
    <div :class="{'ly-is-full':isFull}">
        <div class="tableSelect" ref="tableSelect">
            <el-form :inline="true" :model="formInline" label-position="left">
                <el-form-item label="主机：">
                    <el-input size="default" v-model.trim="formInline.search" maxlength="60"  clearable placeholder="服务器IP/域名" @change="search" style="width:200px"></el-input>
                </el-form-item>
                <el-form-item label="" v-show="hasPermission('terminal','Search')"><el-button  @click="search" type="primary" icon="Search">查询</el-button></el-form-item>
                <el-form-item label=""><el-button  @click="handleEdit('','reset')" icon="Refresh">重置</el-button></el-form-item>
                <el-form-item label="" v-show="hasPermission('terminal','Create')"><el-button type="primary" icon="Plus" @click="addAdmin">新增</el-button></el-form-item>
            </el-form>
        </div>
        <div class="table">
            <el-table  :height="'calc('+(tableHeight)+'px)'" border :data="tableData" ref="tableref" v-loading="loadingPage" style="width: 100%">
                <el-table-column type="index" width="60" align="center" label="序号">
                    <template #default="scope">
                        <span v-text="getIndex(scope.$index)"></span>
                    </template>
                </el-table-column>
                <el-table-column min-width="110" prop="host" label="主机"></el-table-column>
                <el-table-column min-width="110" prop="port" label="端口"></el-table-column>
                <el-table-column min-width="110" prop="remark" label="备注"></el-table-column>
                <el-table-column min-width="100" prop="typename" label="验证方式"></el-table-column>
                <el-table-column min-width="100" prop="username" label="用户名"></el-table-column>
                <el-table-column min-width="150" prop="create_datetime" label="创建时间"></el-table-column>
                <el-table-column label="操作" fixed="right" width="180">
                    <template #header>
                        <div style="display: flex;justify-content: space-between;align-items: center;">
                            <div>操作</div>
                            <div @click="setFull">
                                <el-tooltip content="全屏" placement="bottom">
                                    <el-icon ><full-screen /></el-icon>
                                </el-tooltip>
                            </div>
                        </div>
                    </template>
                    <template #default="scope">
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'openterminal')" v-show="hasPermission('terminal','Update')">打开终端</span>
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'edit')" v-show="hasPermission('terminal','Update')">编辑</span>
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'delete')" v-show="hasPermission('terminal','Delete')">删除</span>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <Pagination v-bind:child-msg="pageparm" @callFather="callFather"></Pagination>
        <add-module-terminal ref="addModuleTerminalFlag" @refreshData="getData"></add-module-terminal>

    </div>
</template>

<script>
    import Pagination from "@/components/Pagination.vue";
    import {dateFormats,getTableHeight} from "@/utils/util";
    import LyXterm from "@/components/terminal/xterm.vue";
    import {apiTerminal,apiTerminalDelete} from '@/api/api'
    import AddModuleTerminal from "./components/addModuleTerminal.vue";
    import {domain} from '@/api/url'
    export default {
        name: "terminal",
        components: {AddModuleTerminal, LyXterm, Pagination},
        data(){
            return{
                isFull:false,
                tableHeight:500,
                loadingPage:false,
                formInline:{
                    page: 1,
                    limit: 10,
                },
                pageparm: {
                    page: 1,
                    limit: 10,
                    total: 0
                },
                timers:[],
                tableData:[],
            }
        },
        methods:{
            // 表格序列号
            getIndex($index) {
                // (当前页 - 1) * 当前显示数据条数 + 当前行数据的索引 + 1
                return (this.pageparm.page-1)*this.pageparm.limit + $index +1
            },
            setFull(){
                this.isFull=!this.isFull
                window.dispatchEvent(new Event('resize'))
            },
            changeStatus(row) {
                // console.log(row,'row----')
            },
            addAdmin() {
                this.$refs.addModuleTerminalFlag.addUserFn(null,'新增')
            },
            handleEdit(row,flag) {
                if(flag=='edit') {
                    this.$refs.addModuleTerminalFlag.addUserFn(row,'编辑')
                }
                else if(flag=='openterminal') {
                    let baseurl = window.location.protocol+"//"+window.location.host
                    window.open(baseurl+"/#/lyterminal?id="+row.id+"&host="+row.host,'_blank');
                }
                else if(flag=='delete') {
                    let vm = this
                    vm.$confirm('您确定要删除选中的数据吗？',{
                        closeOnClickModal:false
                    }).then(res=>{
                        apiTerminalDelete({id:row.id}).then(res=>{
                            if(res.code == 2000) {
                                vm.$message.success(res.msg)
                                vm.search()
                            } else {
                                vm.$message.warning(res.msg)
                            }
                        })
                    }).catch(()=>{

                    })
                }
                else if(flag=="reset"){
                    this.formInline = {
                        page:1,
                        limit: 10
                    }
                    this.pageparm={
                        page: 1,
                        limit: 10,
                        total: 0
                    }
                    this.getData()
                }
            },
            /**
             * 从URL里下载文件
            */
            // 下载文件
            downloadFileURL(url) {
                var iframe =document.createElement("iframe")
                iframe.style.display ="none";
                iframe.src = url;
                document.body.appendChild(iframe);
            },
            exportDataBackend() {
                // var params = {
                //     page: 1,
                //     limit: 9999,
                // }
                // UsersUsersExportexecl(params).then(res => {
                //      if(res.code ==2000) {
                //          this.downloadFileURL(res.data.data)
                //          //this.$message.warning(res.data.data)
                //      }
                //  })
            },
            callFather(parm) {
                this.formInline.page = parm.page
                this.formInline.limit = parm.limit
                this.getData()
            },
            search() {
                this.formInline.page = 1
                this.formInline.limit = 10
                this.getData()
            },
            //获取列表
            async getData() {
                this.loadingPage = true
                apiTerminal(this.formInline).then(res => {
                     this.loadingPage = false
                     if(res.code ==2000) {
                         this.tableData = res.data.data
                         this.pageparm.page = res.data.page;
                         this.pageparm.limit = res.data.limit;
                         this.pageparm.total = res.data.total;
                     }
                 })
            },

            timeChange(val){
                if (val) {
                    this.formInline.beginAt=dateFormats(val[0],'yyyy-MM-dd hh:mm:ss');
                    this.formInline.endAt=dateFormats(val[1],'yyyy-MM-dd hh:mm:ss');
                } else {
                    this.formInline.beginAt = null
                    this.formInline.endAt = null
                }
                this.search()
            },
            // 计算搜索栏的高度
            listenResize() {
				this.$nextTick(() => {
				    this.getTheTableHeight()
				})
			},
            getTheTableHeight(){
                let tabSelectHeight = this.$refs.tableSelect?this.$refs.tableSelect.offsetHeight:0
                tabSelectHeight = this.isFull?tabSelectHeight - 110:tabSelectHeight
                this.tableHeight =  getTableHeight(tabSelectHeight)
            }

        },
        created() {
            this.getData()
        },
        mounted() {
            // 监听页面宽度变化搜索框的高度
            window.addEventListener('resize', this.listenResize);
            this.$nextTick(() => {
                this.getTheTableHeight()
            })
        },

        unmounted() {
             // 页面销毁，去掉监听事件
			window.removeEventListener("resize", this.listenResize);
        },

    }
</script>

<style lang="scss" scoped>
    .lycontainer{
        background: var(--el-bg-color);
        padding: 10px;
        height: calc(100vh - 220px) ;
        /*background: black;*/
        /*padding: 10px;*/
    }
    ::v-deep(.el-tabs__header){
        margin: 0 0 1px;
    }
</style>