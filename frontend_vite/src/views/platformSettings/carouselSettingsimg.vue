<template>
    <div>
        <el-tabs v-model="formInline.type"  @tab-click="handleClick">
            <el-tab-pane label="首页轮播图管理" name="1"></el-tab-pane>
            <el-tab-pane label="分类页轮播图管理" name="2"></el-tab-pane>
        </el-tabs>
        <el-table :height="'calc('+(tableHeight)+'px)'" border :data="tableData" ref="tableref" v-loading="loadingPage" style="width: 100%">

            <el-table-column type="index" width="60" align="center" label="序号"></el-table-column>
            <el-table-column min-width="120" prop="image" :label="(formInline.type==1) ? '图片' :'图片'">
                <template #default="scope">
                    <el-image  :src="scope.row.image" style="width: 40px;height: 40px" :preview-src-list="[scope.row.image]"  :preview-teleported="true"></el-image>
                </template>
            </el-table-column>
            <el-table-column min-width="150" prop="title" label="标题" ></el-table-column>
            <el-table-column min-width="150" prop="link" label="链接" ></el-table-column>
            <el-table-column min-width="150" prop="sort" label="排序" ></el-table-column>
            <el-table-column min-width="100" label="状态">
                <template #default="scope">
                    <el-tag v-if="scope.row.status">正常</el-tag>
                    <el-tag v-else type="danger">禁用</el-tag>
                </template>
            </el-table-column>
            <el-table-column min-width="150" prop="create_datetime" label="创建时间"></el-table-column>
            <el-table-column label="操作" fixed="right" width="180">
                <template #header>
                    <el-button  size="small" @click="addModule" type="primary" v-show="isShowBtn('carouselSettingsimg','轮播图设置','Create')">新增</el-button>
                </template>
                <template #default="scope">
                    <!--v-show="isShowBtn('dynamicsInfo','平台图片设置','Update')"-->
                    <span class="table-operate-btn" @click="handleEdit(scope.row,'edit')" v-show="isShowBtn('carouselSettingsimg','轮播图设置','Update')">编辑</span>
                    <span class="table-operate-btn" @click="handleEdit(scope.row,'delete')" v-show="isShowBtn('carouselSettingsimg','轮播图设置','Delete')">删除</span>
                </template>
            </el-table-column>
        </el-table>
        <Pagination v-bind:child-msg="pageparm" @callFather="callFather"></Pagination>
        <add-module ref="addModuleFlag" @refreshData="getData"></add-module>
    </div>

</template>
<script>
    import addModule from "./components/addCarouselModule.vue";
    import Pagination from "@/components/Pagination.vue";
    import {dateFormats,getTableHeight} from "@/utils/util";
    import {platformsettingsLunboimg,platformsettingsLunboimgDelete} from '@/api/api'
    export default {
        components:{
            Pagination,
            addModule
        },
        name:'carouselSettingsimg',
        data() {
            return {
                isFull:false,
                tableHeight:500,
                loadingPage:false,
                formInline:{
                    type:'1',// 【参数】type轮播图类型: 1为首页轮播图，2为分类页轮播图
                },
                pageparm: {
                    page: 1,
                    limit: 10,
                    total: 0
                },
                statusList:[
                    {id:1,name:'是'},
                    {id:0,name:'否'}
                ],
                tableData:[]
            }
        },
        methods:{
            setFull(){
                this.isFull=!this.isFull
                window.dispatchEvent(new Event('resize'))
            },
            handleClick(tab,e) {
                this.formInline.type = tab.props.name
                this.search()
            },
            addModule() {
                this.$refs.addModuleFlag.addModuleFn(null,'新增',this.formInline.type)
            },
            changeStatus(row) {
                // console.log(row,'row----')
            },
            handleEdit(row,flag) {
                let vm = this
                if(flag=='edit') {
                    vm.$refs.addModuleFlag.addModuleFn(row,'编辑',this.formInline.type)
                }
                if(flag=='delete') {
                    vm.$confirm('您确定要删除选中的内容？',{
                        closeOnClickModal:false
                    }).then(res=>{
                        if(this.formInline.type==1 || this.formInline.type==2) {
                            platformsettingsLunboimgDelete({id:row.id}).then(res=>{
                                if(res.code == 2000) {
                                    vm.$message.success(res.msg)
                                    vm.search()
                                } else {
                                    vm.$message.warning(res.msg)
                                }
                            })
                        }
                    }).catch(()=>{

                    })
                }
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
            async getData(){
                this.loadingPage = true
                if(this.formInline.type==1 || this.formInline.type==2) {
                    platformsettingsLunboimg(this.formInline).then(res => {
                        this.loadingPage = false
                        if(res.code ==2000) {
                            this.tableData = res.data.data
                            this.pageparm.page = res.data.page;
                            this.pageparm.limit = res.data.limit;
                            this.pageparm.total = res.data.total;
                        }
                    })
                }
            },
            // 计算搜索栏的高度
            listenResize() {
				this.$nextTick(() => {
				    this.getTheTableHeight()
				})
			},
            getTheTableHeight(){
                let tabSelectHeight = 43
                tabSelectHeight = this.isFull?tabSelectHeight - 100:tabSelectHeight
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


