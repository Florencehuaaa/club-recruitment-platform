from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# 模拟数据
社团数据 = [
    {
        "id": 1,
        "名称": "计算机协会",
        "类型": "科技",
        "简介": "专注于计算机技术学习与交流的社团，定期举办技术讲座和编程比赛。",
        "成员规模": 120,
        "活动频率": "每周2次",
        "标签": ["编程", "技术", "算法", "人工智能"],
        "招新要求": "对计算机技术有兴趣，有一定编程基础者优先。",
        "联系方式": "computer@example.com",
        "活动历史": ["2024年编程大赛", "2024年技术讲座系列"],
        "热度": 95,
        "图片": "https://copilot-cn.bytedance.net/api/ide/v1/text_to_image?prompt=computer%20science%20club%20students%20coding%20together&image_size=square_hd"
    },
    {
        "id": 2,
        "名称": "摄影协会",
        "类型": "艺术",
        "简介": "热爱摄影的同学组成的社团，定期组织外出拍摄和作品展览。",
        "成员规模": 80,
        "活动频率": "每周1次",
        "标签": ["摄影", "艺术", "美学", "创作"],
        "招新要求": "对摄影有兴趣，有无相机均可。",
        "联系方式": "photo@example.com",
        "活动历史": ["2024年校园摄影展", "2024年户外拍摄活动"],
        "热度": 85,
        "图片": "https://copilot-cn.bytedance.net/api/ide/v1/text_to_image?prompt=photography%20club%20students%20taking%20photos%20outdoors&image_size=square_hd"
    },
    {
        "id": 3,
        "名称": "辩论社",
        "类型": "学术",
        "简介": "培养辩论能力和逻辑思维的社团，参加各类辩论赛。",
        "成员规模": 50,
        "活动频率": "每周2次",
        "标签": ["辩论", "逻辑", "演讲", "表达"],
        "招新要求": "思维敏捷，表达能力强，对辩论有兴趣。",
        "联系方式": "debate@example.com",
        "活动历史": ["2024年校际辩论赛", "2024年辩论技巧培训"],
        "热度": 80,
        "图片": "https://copilot-cn.bytedance.net/api/ide/v1/text_to_image?prompt=debate%20club%20students%20arguing%20in%20competition&image_size=square_hd"
    },
    {
        "id": 4,
        "名称": "足球社",
        "类型": "体育",
        "简介": "热爱足球的同学组成的社团，定期组织训练和比赛。",
        "成员规模": 60,
        "活动频率": "每周3次",
        "标签": ["足球", "体育", "团队", "竞技"],
        "招新要求": "对足球有兴趣，有一定基础者优先。",
        "联系方式": "football@example.com",
        "活动历史": ["2024年校内足球联赛", "2024年足球技巧培训"],
        "热度": 90,
        "图片": "https://copilot-cn.bytedance.net/api/ide/v1/text_to_image?prompt=football%20club%20students%20playing%20soccer%20on%20field&image_size=square_hd"
    },
    {
        "id": 5,
        "名称": "文学社",
        "类型": "文学",
        "简介": "热爱文学的同学组成的社团，定期举办读书分享和写作活动。",
        "成员规模": 70,
        "活动频率": "每周1次",
        "标签": ["文学", "写作", "阅读", "交流"],
        "招新要求": "对文学有兴趣，喜欢阅读和写作。",
        "联系方式": "literature@example.com",
        "活动历史": ["2024年读书分享会", "2024年校园文学创作大赛"],
        "热度": 75,
        "图片": "https://copilot-cn.bytedance.net/api/ide/v1/text_to_image?prompt=literature%20club%20students%20reading%20and%20discussing%20books&image_size=square_hd"
    }
]

用户数据 = []
报名数据 = []
活动数据 = []

# 智能匹配算法
def 智能匹配(用户兴趣, 社团列表):
    匹配结果 = []
    for 社团 in 社团列表:
        匹配度 = 0
        for 兴趣 in 用户兴趣:
            if 兴趣 in 社团["标签"]:
                匹配度 += 20
        # 考虑热度因素
        匹配度 += 社团["热度"] * 0.1
        社团["匹配度"] = 匹配度
        匹配结果.append(社团)
    # 按匹配度排序
    匹配结果.sort(key=lambda x: x["匹配度"], reverse=True)
    return 匹配结果

# 路由
@app.route('/')
def index():
    return "社团招新智能匹配平台后端服务"

# 获取所有社团
@app.route('/api/社团列表', methods=['GET'])
def 获取社团列表():
    return jsonify(社团数据)

# 获取社团详情
@app.route('/api/社团详情/<int:id>', methods=['GET'])
def 获取社团详情(id):
    for 社团 in 社团数据:
        if 社团["id"] == id:
            return jsonify(社团)
    return jsonify({"error": "社团不存在"}), 404

# 智能匹配
@app.route('/api/智能匹配', methods=['POST'])
def 进行智能匹配():
    数据 = request.json
    用户兴趣 = 数据.get("兴趣", [])
    匹配结果 = 智能匹配(用户兴趣, 社团数据)
    return jsonify(匹配结果)

# 用户注册
@app.route('/api/注册', methods=['POST'])
def 注册():
    数据 = request.json
    用户名 = 数据.get("用户名")
    密码 = 数据.get("密码")
    学号 = 数据.get("学号")
    兴趣 = 数据.get("兴趣", [])
    
    # 检查用户是否已存在
    for 用户 in 用户数据:
        if 用户["学号"] == 学号:
            return jsonify({"error": "用户已存在"}), 400
    
    新用户 = {
        "id": len(用户数据) + 1,
        "用户名": 用户名,
        "密码": 密码,
        "学号": 学号,
        "兴趣": 兴趣
    }
    用户数据.append(新用户)
    return jsonify({"message": "注册成功", "用户": 新用户})

# 用户登录
@app.route('/api/登录', methods=['POST'])
def 登录():
    数据 = request.json
    学号 = 数据.get("学号")
    密码 = 数据.get("密码")
    
    for 用户 in 用户数据:
        if 用户["学号"] == 学号 and 用户["密码"] == 密码:
            return jsonify({"message": "登录成功", "用户": 用户})
    return jsonify({"error": "学号或密码错误"}), 401

# 报名社团
@app.route('/api/报名', methods=['POST'])
def 报名():
    数据 = request.json
    用户id = 数据.get("用户id")
    社团id = 数据.get("社团id")
    
    # 检查用户是否存在
    用户存在 = False
    for 用户 in 用户数据:
        if 用户["id"] == 用户id:
            用户存在 = True
            break
    if not 用户存在:
        return jsonify({"error": "用户不存在"}), 404
    
    # 检查社团是否存在
    社团存在 = False
    for 社团 in 社团数据:
        if 社团["id"] == 社团id:
            社团存在 = True
            break
    if not 社团存在:
        return jsonify({"error": "社团不存在"}), 404
    
    # 检查是否已经报名
    for 报名 in 报名数据:
        if 报名["用户id"] == 用户id and 报名["社团id"] == 社团id:
            return jsonify({"error": "已经报名该社团"}), 400
    
    新报名 = {
        "id": len(报名数据) + 1,
        "用户id": 用户id,
        "社团id": 社团id,
        "状态": "待审核"
    }
    报名数据.append(新报名)
    return jsonify({"message": "报名成功", "报名": 新报名})

# 获取用户报名状态
@app.route('/api/报名状态/<int:user_id>', methods=['GET'])
def 获取报名状态(user_id):
    用户报名 = []
    for 报名 in 报名数据:
        if 报名["用户id"] == user_id:
            # 获取社团信息
            社团信息 = None
            for 社团 in 社团数据:
                if 社团["id"] == 报名["社团id"]:
                    社团信息 = 社团
                    break
            if 社团信息:
                用户报名.append({
                    "报名id": 报名["id"],
                    "社团": 社团信息,
                    "状态": 报名["状态"]
                })
    return jsonify(用户报名)

# 发布活动
@app.route('/api/发布活动', methods=['POST'])
def 发布活动():
    数据 = request.json
    标题 = 数据.get("标题")
    描述 = 数据.get("描述")
    时间 = 数据.get("时间")
    地点 = 数据.get("地点")
    社团id = 数据.get("社团id")
    类型 = 数据.get("类型")
    要求 = 数据.get("要求")
    
    # 检查社团是否存在
    社团存在 = False
    for 社团 in 社团数据:
        if 社团["id"] == 社团id:
            社团存在 = True
            break
    if not 社团存在:
        return jsonify({"error": "社团不存在"}), 404
    
    新活动 = {
        "id": len(活动数据) + 1,
        "标题": 标题,
        "描述": 描述,
        "时间": 时间,
        "地点": 地点,
        "社团id": 社团id,
        "类型": 类型,
        "要求": 要求,
        "报名人数": 0,
        "报名列表": []
    }
    活动数据.append(新活动)
    return jsonify({"message": "活动发布成功", "活动": 新活动})

# 获取活动列表
@app.route('/api/活动列表', methods=['GET'])
def 获取活动列表():
    # 可选的类型筛选
    类型 = request.args.get('类型')
    if 类型:
        筛选活动 = [活动 for 活动 in 活动数据 if 活动.get("类型") == 类型]
        return jsonify(筛选活动)
    return jsonify(活动数据)

# 获取活动详情
@app.route('/api/活动详情/<int:id>', methods=['GET'])
def 获取活动详情(id):
    for 活动 in 活动数据:
        if 活动["id"] == id:
            # 获取社团信息
            社团信息 = None
            for 社团 in 社团数据:
                if 社团["id"] == 活动["社团id"]:
                    社团信息 = 社团
                    break
            if 社团信息:
                活动["社团"] = 社团信息
            return jsonify(活动)
    return jsonify({"error": "活动不存在"}), 404

# 报名活动
@app.route('/api/报名活动', methods=['POST'])
def 报名活动():
    数据 = request.json
    用户id = 数据.get("用户id")
    活动id = 数据.get("活动id")
    
    # 检查用户是否存在
    用户存在 = False
    for 用户 in 用户数据:
        if 用户["id"] == 用户id:
            用户存在 = True
            break
    if not 用户存在:
        return jsonify({"error": "用户不存在"}), 404
    
    # 检查活动是否存在
    活动存在 = False
    活动索引 = -1
    for i, 活动 in enumerate(活动数据):
        if 活动["id"] == 活动id:
            活动存在 = True
            活动索引 = i
            break
    if not 活动存在:
        return jsonify({"error": "活动不存在"}), 404
    
    # 检查是否已经报名
    if 用户id in 活动数据[活动索引]["报名列表"]:
        return jsonify({"error": "已经报名该活动"}), 400
    
    # 添加报名
    活动数据[活动索引]["报名列表"].append(用户id)
    活动数据[活动索引]["报名人数"] = len(活动数据[活动索引]["报名列表"])
    
    return jsonify({"message": "报名成功", "活动": 活动数据[活动索引]})

# 取消报名活动
@app.route('/api/取消报名活动', methods=['POST'])
def 取消报名活动():
    数据 = request.json
    用户id = 数据.get("用户id")
    活动id = 数据.get("活动id")
    
    # 检查活动是否存在
    活动存在 = False
    活动索引 = -1
    for i, 活动 in enumerate(活动数据):
        if 活动["id"] == 活动id:
            活动存在 = True
            活动索引 = i
            break
    if not 活动存在:
        return jsonify({"error": "活动不存在"}), 404
    
    # 检查是否已经报名
    if 用户id not in 活动数据[活动索引]["报名列表"]:
        return jsonify({"error": "未报名该活动"}), 400
    
    # 取消报名
    活动数据[活动索引]["报名列表"].remove(用户id)
    活动数据[活动索引]["报名人数"] = len(活动数据[活动索引]["报名列表"])
    
    return jsonify({"message": "取消报名成功", "活动": 活动数据[活动索引]})

# 获取活动报名统计
@app.route('/api/活动统计/<int:activity_id>', methods=['GET'])
def 获取活动统计(activity_id):
    for 活动 in 活动数据:
        if 活动["id"] == activity_id:
            return jsonify({
                "活动id": 活动["id"],
                "标题": 活动["标题"],
                "报名人数": 活动["报名人数"],
                "报名列表": 活动["报名列表"]
            })
    return jsonify({"error": "活动不存在"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)