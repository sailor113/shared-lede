#!/bin/sh

# 下载源码
SWITCH_TAG_FLAG=false
git clone --single-branch -b openwrt-23.05 https://git.openwrt.org/openwrt/openwrt.git
if $SWITCH_TAG_FLAG; then
    cd openwrt
    LATEST_TAG=$(git tag | awk 'END {print}')
    git checkout $LATEST_TAG
    echo "已切换到最近稳定版本$LATEST_TAG"
    cd ..
fi
mv ./openwrt/* ./

# 下载插件
SUPPLY_DIR=supply-packages
echo "src-link supply $PWD/$SUPPLY_DIR" >> feeds.conf.default
mkdir $SUPPLY_DIR && cd $SUPPLY_DIR
git clone --depth 1 https://github.com/jerrykuku/luci-theme-argon.git
git clone --depth 1 https://github.com/jerrykuku/luci-app-argon-config.git
git clone --depth 1 https://github.com/yichya/luci-app-xray.git
git clone --depth 1 https://github.com/xiaorouji/openwrt-passwall-packages.git pw-dependencies
svn export https://github.com/xiaorouji/openwrt-passwall/trunk/luci-app-passwall
svn export https://github.com/xiaorouji/openwrt-passwall2/trunk/luci-app-passwall2
svn export https://github.com/vernesong/OpenClash/trunk/luci-app-openclash
