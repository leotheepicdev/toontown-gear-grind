from panda3d.core import ClockObject, Mat3, NodePath, Point3, Vec3
from direct.controls.GravityWalker import GravityWalker
from direct.showbase.InputStateGlobal import inputState
from direct.task.Task import Task
from otp.otpbase import OTPGlobals

class GravityWalker(GravityWalker):

    def handleAvatarControls(self, task):
        run = inputState.isSet('run')
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        turnLeft = inputState.isSet('turnLeft')
        turnRight = inputState.isSet('turnRight')
        slideLeft = inputState.isSet('slideLeft')
        slideRight = inputState.isSet('slideRight')
        jump = inputState.isSet('jump')
        sprint = inputState.isSet('sprint')
        hasLocal = 'localAvatar' in __builtins__ and base.localAvatar
        if hasLocal and base.localAvatar.getAutoRun():
            forward = 1
            reverse = 0
        self.speed = forward and self.avatarControlForwardSpeed or reverse and -self.avatarControlReverseSpeed
        self.slideSpeed = reverse and slideLeft and -self.avatarControlReverseSpeed * 0.75 or reverse and slideRight and self.avatarControlReverseSpeed * 0.75 or slideLeft and -self.avatarControlForwardSpeed * 0.75 or slideRight and self.avatarControlForwardSpeed * 0.75
        self.rotationSpeed = not (slideLeft or slideRight) and (turnLeft and self.avatarControlRotateSpeed or turnRight and -self.avatarControlRotateSpeed)
        if self.speed and self.slideSpeed:
            self.speed *= GravityWalker.DiagonalFactor
            self.slideSpeed *= GravityWalker.DiagonalFactor
        debugRunning = inputState.isSet('debugRunning')
        if debugRunning:
            self.speed *= base.debugRunningMultiplier
            self.slideSpeed *= base.debugRunningMultiplier
            self.rotationSpeed *= 1.25
        if sprint and not base.localAvatar.chatMgr.chatInputWhiteList.isActive() and not base.localAvatar.isDisguised and (self.speed or self.slideSpeed or self.rotationSpeed):
            self.speed *= OTPGlobals.ToonSprintSpeedMult
            if hasLocal:
                base.localAvatar.startSprinting()
        else:
            if hasLocal:
                base.localAvatar.stopSprinting()
        if self.needToDeltaPos:
            self.setPriorParentVector()
            self.needToDeltaPos = 0
        if self.wantDebugIndicator:
            self.displayDebugInfo()
        if self.lifter.isOnGround():
            if self.isAirborne:
                self.isAirborne = 0
                impact = self.lifter.getImpactVelocity()
                if impact < -30.0:
                    messenger.send('jumpHardLand')
                    self.startJumpDelay(0.3)
                else:
                    messenger.send('jumpLand')
                    if impact < -5.0:
                        self.startJumpDelay(0.2)
            self.priorParent = Vec3.zero()
            if jump and self.mayJump:
                self.lifter.addVelocity(self.avatarControlJumpForce)
                messenger.send('jumpStart')
                self.isAirborne = 1
        elif self.isAirborne == 0:
            pass
        else:
            self.isAirborne = 1

        self.__oldPosDelta = self.avatarNodePath.getPosDelta(render)
        self.__oldDt = ClockObject.getGlobalClock().getDt()
        dt = self.__oldDt
        self.moving = self.speed or self.slideSpeed or self.rotationSpeed or self.priorParent != Vec3.zero()
        if self.moving:
            distance = dt * self.speed
            slideDistance = dt * self.slideSpeed
            rotation = dt * self.rotationSpeed
            if distance or slideDistance or self.priorParent != Vec3.zero():
                rotMat = Mat3.rotateMatNormaxis(self.avatarNodePath.getH(), Vec3.up())
                if self.isAirborne:
                    forward = Vec3.forward()
                else:
                    contact = self.lifter.getContactNormal()
                    forward = contact.cross(Vec3.right())
                    forward.normalize()
                self.vel = Vec3(forward * distance)
                if slideDistance:
                    if self.isAirborne:
                        right = Vec3.right()
                    else:
                        right = forward.cross(contact)
                        right.normalize()
                    self.vel = Vec3(self.vel + right * slideDistance)
                self.vel = Vec3(rotMat.xform(self.vel))
                step = self.vel + self.priorParent * dt
                self.avatarNodePath.setFluidPos(Point3(self.avatarNodePath.getPos() + step))
            self.avatarNodePath.setH(self.avatarNodePath.getH() + rotation)
        else:
            self.vel.set(0.0, 0.0, 0.0)
        if self.moving or jump:
            messenger.send('avatarMoving')
        return Task.cont